"""Run YCSB against a BONDI deployment or database connection."""

import json
import re
import subprocess
from dataclasses import asdict, dataclass, field
from pathlib import Path
from tempfile import mkdtemp
from typing import Self
from urllib.parse import parse_qsl, quote, unquote, urlencode, urlsplit, urlunsplit

from bondi import CouchbaseConnection, MongoConnection
from bondi.deployment import Deployment

from ._results import BenchmarkError, Result, parse_result

__all__ = ["YCSB", "BenchmarkError", "Result", "Workload"]

IMAGE = "ghcr.io/relaxed-constraints/bondi-benchmarks/ycsb:0.1.0"
# These values come from the selected target and the typed workload arguments.
RUNNER_PROPERTIES = {
    "recordcount",
    "operationcount",
    "threadcount",
    "target",
    "mongodb.url",
    "couchbase.host",
    "couchbase.bucket",
    "couchbase.username",
    "couchbase.password",
}


@dataclass(frozen=True)
class Workload:
    profile: str
    record_count: int
    operation_count: int
    threads: int = 1
    target_ops_s: int | None = None
    properties: dict[str, str | int | float | bool] = field(default_factory=dict)

    def __post_init__(self):
        if self.profile not in tuple("ABCDEF"):
            raise ValueError("profile must be one of A through F")
        counts = [self.record_count, self.operation_count, self.threads]
        if self.target_ops_s is not None:
            counts.append(self.target_ops_s)
        for n in counts:
            if type(n) is not int or n <= 0:
                raise ValueError("Counts, threads and target throughput must be positive integers")
        for key, value in self.properties.items():
            if not isinstance(key, str) or not key:
                raise ValueError("YCSB property names must be nonempty strings")
            if key in RUNNER_PROPERTIES:
                raise ValueError(f"{key} is set by the runner's workload or connection arguments")
            if not isinstance(value, (str, int, float, bool)):
                raise TypeError(f"{key} requires a string, number, or boolean")


def _docker(*args):
    try:
        result = subprocess.run(["docker", *args], text=True, capture_output=True, check=True)
    except subprocess.CalledProcessError as exc:
        raise BenchmarkError(f"Docker {args[0]} failed", exc.stdout, exc.stderr) from exc
    except FileNotFoundError as exc:
        raise BenchmarkError("Docker CLI was not found") from exc
    return result.stdout.strip()


def _runner_image_id(image):
    inspect = ("image", "inspect", "--format", "{{.Id}}", image)
    try:
        return _docker(*inspect)
    except BenchmarkError as exc:
        # An unavailable daemon or a permissions error is not a cache miss.
        if not any(
            line.startswith(("Error: No such image:", "Error response from daemon: No such image:"))
            for line in exc.stderr.splitlines()
        ):
            raise

    print(f"Downloading YCSB runner {image}", flush=True)
    try:
        _docker("pull", image)
    except BenchmarkError as exc:
        raise BenchmarkError(
            f"Could not pull YCSB runner {image}: {exc.stderr.strip() or exc}",
            exc.stdout,
            exc.stderr,
        ) from exc
    return _docker(*inspect)


def _managed_network(deployment):
    # BONDI publishes its service on a unique loopback port. Sharing the service's
    # network namespace also makes Couchbase's advertised local address reachable.
    internal = 27017 if deployment.backend == "mongodb" else 8091
    mapping = f"127.0.0.1:{deployment.port}->{internal}/tcp"
    rows = _docker(
        "ps",
        "--filter",
        f"label=com.docker.compose.service={deployment.backend}",
        "--format",
        "{{.ID}} {{.Ports}}",
    )
    matches = [row.split()[0] for row in rows.splitlines() if mapping in row]
    if len(matches) != 1:
        raise BenchmarkError(f"Expected one running {deployment.backend} service at {mapping}")
    return "container:" + matches[0]


def _mongo_uri(conn, endpoint, database):
    original = urlsplit(conn.uri)
    runner = urlsplit(endpoint or conn.uri)
    if original.scheme not in {"mongodb", "mongodb+srv"} or runner.scheme != original.scheme:
        raise ValueError(
            "Use mongodb:// or mongodb+srv:// and preserve the scheme in endpoint overrides"
        )
    username = conn.username if conn.username is not None else unquote(original.username or "")
    password = conn.password if conn.password is not None else unquote(original.password or "")
    hosts = runner.netloc.rsplit("@", 1)[-1]
    options = parse_qsl(original.query, keep_blank_values=True)
    if (
        original.scheme == "mongodb"
        and username
        and not any(k.lower() == "authsource" for k, _ in options)
    ):
        options.append(("authSource", unquote(original.path.strip("/")) or "admin"))
    auth = f"{quote(username, safe='')}:{quote(password, safe='')}@" if username else ""
    return urlunsplit((original.scheme, auth + hosts, "/" + database, urlencode(options), ""))


def _empty_target(conn, database, table):
    if isinstance(conn, MongoConnection):
        from bondi.mongodb import MongoExecutor

        with MongoExecutor.from_connection(conn) as executor:
            return executor.client[database][table].find_one({}, {"_id": 1}) is None

    from bondi.couchbase import CouchbaseExecutor
    from couchbase.kv_range_scan import RangeScan
    from couchbase.options import ScanOptions

    with CouchbaseExecutor.from_connection(conn) as executor:
        collection = executor.cluster.bucket(database).default_collection()
        return next(iter(collection.scan(RangeScan(), ScanOptions(ids_only=True))), None) is None


def _properties(values):
    # Java Properties.load(InputStream) reads Latin-1 and interprets backslash escapes.
    def encode(value):
        if isinstance(value, bool):
            value = str(value).lower()
        data = str(value).encode("utf-16-be")
        return "".join(f"\\u{data[i : i + 2].hex()}" for i in range(0, len(data), 2))

    lines = []
    for key, value in values.items():
        name = key if re.fullmatch(r"[A-Za-z0-9_.-]+", key) else encode(key)
        lines.append(f"{name}={encode(value)}\n")
    return "".join(lines)


class YCSB:
    """Run YCSB using a connection or a local BONDI deployment."""

    def __init__(self, *args, **kwargs):
        raise TypeError("Use YCSB.from_connection() or YCSB.from_deployment()")

    @classmethod
    def from_connection(
        cls,
        connection: MongoConnection | CouchbaseConnection,
        database: str,
        *,
        runner_endpoint: str | None = None,
        image: str = IMAGE,
        artifact_dir: str | Path | None = None,
    ) -> Self:
        """Use an existing database reachable from the host and the Docker runner.

        During load, Python checks the destination using the host connection.
        The benchmark client runs on Docker's bridge network and must reach the
        same database and its advertised service addresses. Inside the runner,
        localhost points to the runner itself. Supply runner_endpoint when the
        same database has a different address from inside Docker.
        """
        if not isinstance(connection, (MongoConnection, CouchbaseConnection)):
            raise TypeError("Expected a MongoConnection or CouchbaseConnection")
        return cls._create(connection, None, database, runner_endpoint, image, artifact_dir)

    @classmethod
    def from_deployment(
        cls,
        deployment: Deployment,
        database: str,
        *,
        image: str = IMAGE,
        artifact_dir: str | Path | None = None,
    ) -> Self:
        """Use a running BONDI deployment on the same local Docker engine.

        Python uses the deployment's host-facing connection for the load check.
        Each YCSB container shares the database container's network namespace
        and connects to its internal port over loopback. The caller manages
        the database deployment's lifecycle.
        """
        if not isinstance(deployment, Deployment):
            raise TypeError("Expected a BONDI Deployment")
        return cls._create(deployment.connection, deployment, database, None, image, artifact_dir)

    @classmethod
    def _create(
        cls, connection, deployment, database, runner_endpoint, image, artifact_dir
    ) -> Self:
        if not re.fullmatch(r"[A-Za-z0-9_-]+", database) or database in {
            "admin",
            "local",
            "config",
        }:
            raise ValueError("Choose a dedicated benchmark database or bucket")
        self = object.__new__(cls)
        self._connection = connection
        self._deployment = deployment
        self.database = database
        self.runner_endpoint = runner_endpoint
        self.image = image
        self.artifact_dir = Path(artifact_dir) if artifact_dir is not None else None

        return self

    def load(self, workload: Workload, *, threads: int | None = None) -> Result:
        return self._execute("load", workload, workload.threads if threads is None else threads)

    def run(self, workload: Workload) -> Result:
        return self._execute("run", workload, workload.threads)

    def _execute(self, phase, workload, threads):
        directory = None
        if self.artifact_dir is not None:
            self.artifact_dir.mkdir(parents=True, exist_ok=True)
            directory = Path(mkdtemp(prefix=f"{phase}-", dir=self.artifact_dir))
        try:
            result = self._run_phase(phase, workload, threads)
        except BenchmarkError as exc:
            if directory is not None:
                (directory / "stdout.txt").write_text(exc.stdout, encoding="utf-8")
                (directory / "stderr.txt").write_text(exc.stderr, encoding="utf-8")
                (directory / "error.txt").write_text(str(exc), encoding="utf-8")
            raise
        if directory is not None:
            (directory / "stdout.txt").write_text(result.stdout, encoding="utf-8")
            (directory / "stderr.txt").write_text(result.stderr, encoding="utf-8")
            (directory / "result.json").write_text(
                json.dumps(result.to_dict(), indent=2), encoding="utf-8"
            )
        return result

    def _run_phase(self, phase, workload, threads):
        deployment = self._deployment
        conn = self._connection
        expected = workload.record_count if phase == "load" else workload.operation_count
        if phase == "load":
            expected = int(workload.properties.get("insertcount", expected))
        if type(threads) is not int or not 1 <= threads <= expected:
            raise ValueError("threads must be between 1 and the phase operation count")
        if phase == "load" and not _empty_target(
            conn, self.database, str(workload.properties.get("table", "usertable"))
        ):
            raise BenchmarkError(
                "Benchmark destination contains data. Choose an empty destination."
            )

        image_id = _runner_image_id(self.image)
        network = _managed_network(deployment) if deployment else "bridge"
        endpoint = self.runner_endpoint
        props = dict(
            workload.properties,
            recordcount=workload.record_count,
            operationcount=workload.operation_count,
            threadcount=threads,
        )
        if workload.target_ops_s and phase == "run":
            props["target"] = workload.target_ops_s
        if isinstance(conn, MongoConnection):
            binding = "mongodb"
            endpoint = endpoint or ("mongodb://127.0.0.1" if deployment else conn.uri)
            props["mongodb.url"] = _mongo_uri(conn, endpoint, self.database)
        else:
            binding = "couchbase2"
            endpoint = endpoint or ("couchbase://127.0.0.1" if deployment else conn.uri)
            props.update(
                {
                    "couchbase.host": endpoint,
                    "couchbase.bucket": self.database,
                    "couchbase.username": conn.username,
                    "couchbase.password": conn.password,
                }
            )

        cmd = [
            "docker",
            "run",
            "--rm",
            "-i",
            "--network",
            network,
            image_id,
            binding,
            phase,
            workload.profile.lower(),
        ]
        process = subprocess.run(
            cmd, input=_properties(props), text=True, capture_output=True, check=False
        )

        def sanitize(s):
            s = re.sub(r"mongodb(?:\+srv)?://[^\s]+", "[MongoDB URI]", s)
            if conn.password:
                # A password may itself be a number or a measurement label.
                s = "\n".join(
                    line
                    if re.fullmatch(r"\[[A-Z-]+\], [\w()/%=-]+, [\d.eE+-]+", line)
                    else line.replace(conn.password, "[redacted]")
                    for line in s.split("\n")
                )
            return s

        stdout, stderr = sanitize(process.stdout), sanitize(process.stderr)
        if process.returncode:
            raise BenchmarkError(
                f"{binding} {phase} exited with {process.returncode}", stdout, stderr
            )
        config = {
            "workload": asdict(workload),
            "threads": threads,
            "binding": binding,
            "database": self.database,
            "runner_image_id": image_id,
            "runner_image": self.image,
            "deployment": deployment.name if deployment else None,
            "server_image": deployment.image if deployment else None,
        }
        return parse_result(phase, expected, stdout, stderr, config)
