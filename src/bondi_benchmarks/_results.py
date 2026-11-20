"""Read YCSB's final text measurements independently of Docker or Yanex."""

import math
import re
from dataclasses import asdict, dataclass


class BenchmarkError(RuntimeError):
    """A failed phase with captured, sanitized diagnostic output."""

    def __init__(self, message, stdout="", stderr=""):
        super().__init__(message)
        self.stdout = stdout
        self.stderr = stderr


@dataclass(frozen=True)
class Operation:
    count: int
    statuses: dict[str, int]
    p95_us: float | None
    p99_us: float | None


@dataclass(frozen=True)
class Result:
    phase: str
    throughput_ops_s: float
    operations: dict[str, Operation]
    configuration: dict
    stdout: str
    stderr: str

    def metrics(self):
        metrics = {f"{self.phase}_throughput_ops_s": self.throughput_ops_s}
        for name, op in self.operations.items():
            prefix = f"{self.phase}_{name.lower().replace('-', '_')}"
            metrics[f"{prefix}_operations"] = op.count
            for key in ("p95_us", "p99_us"):
                if (value := getattr(op, key)) is not None:
                    metrics[f"{prefix}_{key}"] = value
        return metrics

    def to_dict(self):
        return {
            "schema_version": 1,
            "phase": self.phase,
            "throughput_ops_s": self.throughput_ops_s,
            "operations": {k: asdict(v) for k, v in self.operations.items()},
            "configuration": self.configuration,
        }


def parse_result(phase, expected, stdout, stderr, configuration):
    rows = {}
    for line in stdout.splitlines():
        match = re.fullmatch(r"\[([^]]+)\], ([^,]+), (.+)", line)
        if match:
            section, metric, value = match.groups()
            rows.setdefault(section, {})[metric] = value

    try:
        throughput = float(rows["OVERALL"]["Throughput(ops/sec)"])
        if not math.isfinite(throughput) or throughput <= 0:
            raise ValueError("Invalid overall throughput")
        operations = {}
        for name in ("INSERT", "READ", "UPDATE", "SCAN", "READ-MODIFY-WRITE"):
            if name not in rows:
                continue
            row = rows[name]
            count = int(row["Operations"])
            statuses = {k[7:]: int(v) for k, v in row.items() if k.startswith("Return=")}
            if any(v for k, v in statuses.items() if k != "OK"):
                raise ValueError(f"{name} returned {statuses}")
            if name != "READ-MODIFY-WRITE" and statuses.get("OK", 0) != count:
                raise ValueError(f"Incomplete {name} status counts")
            percentiles = [
                float(row[k]) if k in row else None
                for k in ("95thPercentileLatency(us)", "99thPercentileLatency(us)")
            ]
            operations[name] = Operation(count, statuses, *percentiles)

        # F measures one logical transaction as a READ, UPDATE and compound latency.
        counts = {k: v.count for k, v in operations.items()}
        completed = sum(counts.values()) - 2 * counts.get("READ-MODIFY-WRITE", 0)
        if completed != expected or (phase == "load" and counts.get("INSERT") != expected):
            raise ValueError(f"Expected {expected} {phase} operations, observed {counts}")
    except (ValueError, KeyError) as exc:
        raise BenchmarkError(f"Invalid {phase} measurements: {exc}", stdout, stderr) from exc
    return Result(phase, throughput, operations, configuration, stdout, stderr)
