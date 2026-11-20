import pytest
from bondi import MongoConnection

from bondi_benchmarks import ycsb
from bondi_benchmarks._results import parse_result
from bondi_benchmarks.ycsb import _mongo_uri, _properties

OUTPUT = """[OVERALL], Throughput(ops/sec), 100.5
[READ], Operations, 20
[READ], 99thPercentileLatency(us), 17
[READ], Return=OK, 20"""


def test_result_metrics():
    result = parse_result("run", 20, OUTPUT, "", {})
    assert result.operations["READ"].p99_us == 17
    assert result.metrics() == {
        "run_throughput_ops_s": 100.5,
        "run_read_operations": 20,
        "run_read_p99_us": 17,
    }
    assert result.to_dict()["schema_version"] == 1


@pytest.mark.parametrize(
    "text",
    [
        OUTPUT.replace("OK", "NOT_FOUND"),
        OUTPUT.replace("OK, 20", "OK, 19"),
        OUTPUT.replace("100.5", "NaN"),
        "",
    ],
)
def test_reject_invalid_measurements(text):
    with pytest.raises(ycsb.BenchmarkError) as caught:
        parse_result("run", 20, text, "", {})
    assert caught.value.stdout == text


def test_preserve_authentication_and_route():
    conn = MongoConnection("mongodb://u:old@localhost:27099/original?w=1", password="p@ss")
    assert _mongo_uri(conn, "mongodb://db:27017", "lab") == (
        "mongodb://u:p%40ss@db:27017/lab?w=1&authSource=original"
    )


def test_properties_escape_newlines_and_unicode():
    assert _properties({"password": " \n\\🦘"}) == (
        "password=" + r"\u0020\u000a\u005c\ud83e\udd98" + "\n"
    )


def test_reserved_property():
    with pytest.raises(ValueError):
        ycsb.Workload("A", 10, 20, properties={"mongodb.url": "other"})


def test_phase_artifacts(tmp_path, monkeypatch):
    benchmark = ycsb.YCSB.from_connection(
        MongoConnection("mongodb://localhost"), "lab", artifact_dir=tmp_path
    )
    workload = ycsb.Workload("C", 20, 20)
    result = parse_result("run", 20, OUTPUT, "diagnostic", {})
    monkeypatch.setattr(benchmark, "_run_phase", lambda *args: result)
    benchmark.run(workload)
    benchmark.run(workload)
    directories = list(tmp_path.glob("run-*"))
    assert len(directories) == 2
    assert (directories[0] / "stdout.txt").read_text() == OUTPUT
    assert (directories[0] / "stderr.txt").read_text() == "diagnostic"
    assert (directories[0] / "result.json").is_file()

    def fail(*args):
        raise ycsb.BenchmarkError("invalid phase", "partial", "failed")

    monkeypatch.setattr(benchmark, "_run_phase", fail)
    with pytest.raises(ycsb.BenchmarkError):
        benchmark.load(workload)
    failed = next(tmp_path.glob("load-*"))
    assert (failed / "stderr.txt").read_text() == "failed"
    assert (failed / "stdout.txt").read_text() == "partial"
    assert (failed / "error.txt").read_text() == "invalid phase"


def test_srv_preserves_seed_and_dns_authentication():
    conn = MongoConnection(
        "mongodb+srv://user:old@seed.example.com/?retryWrites=true", password="p@ss"
    )
    assert _mongo_uri(conn, None, "lab") == (
        "mongodb+srv://user:p%40ss@seed.example.com/lab?retryWrites=true"
    )


def test_srv_explicit_auth_source_and_route():
    conn = MongoConnection("mongodb+srv://seed.example.com/?authSource=users&tls=false")
    assert _mongo_uri(conn, "mongodb+srv://other.example.com", "lab") == (
        "mongodb+srv://other.example.com/lab?authSource=users&tls=false"
    )
    with pytest.raises(ValueError):
        _mongo_uri(conn, "mongodb://other.example.com", "lab")


def test_native_properties_pass_through():
    properties = {
        "writeallfields": True,
        "couchbase.kv": False,
        "updateproportion": 0.25,
        "another.binding.option": "custom",
    }
    workload = ycsb.Workload("A", 10, 20, properties=properties)
    assert _properties(workload.properties) == _properties(
        {
            "writeallfields": "true",
            "couchbase.kv": "false",
            "updateproportion": "0.25",
            "another.binding.option": "custom",
        }
    )


def test_direct_constructor_points_to_factories():
    with pytest.raises(TypeError, match=r"from_connection.*from_deployment"):
        ycsb.YCSB(MongoConnection("mongodb://localhost"), "lab")


@pytest.mark.parametrize("managed", [True, False])
def test_factory_selects_runner_route(managed, monkeypatch):
    from unittest.mock import Mock

    connection = MongoConnection("mongodb://localhost:27029")
    deployment = Mock(spec=ycsb.Deployment)
    deployment.connection = connection
    deployment.name = "local"
    deployment.image = "mongo:test"
    if managed:
        benchmark = ycsb.YCSB.from_deployment(deployment, "lab")
    else:
        benchmark = ycsb.YCSB.from_connection(
            connection, "lab", runner_endpoint="mongodb://db:27029"
        )

    network = Mock(return_value="container:db")
    monkeypatch.setattr(ycsb, "_managed_network", network)
    monkeypatch.setattr(ycsb, "_docker", lambda *args: "image-id")
    run = Mock(return_value=ycsb.subprocess.CompletedProcess([], 0, OUTPUT, ""))
    monkeypatch.setattr(ycsb.subprocess, "run", run)
    result = benchmark.run(ycsb.Workload("C", 20, 20))
    cmd = run.call_args.args[0]
    assert cmd[cmd.index("--network") + 1] == ("container:db" if managed else "bridge")
    uri = "mongodb://127.0.0.1/lab" if managed else "mongodb://db:27029/lab"
    assert _properties({"mongodb.url": uri}) in run.call_args.kwargs["input"]
    assert result.configuration["deployment"] == ("local" if managed else None)
    if managed:
        network.assert_called_once_with(deployment)
    else:
        network.assert_not_called()
