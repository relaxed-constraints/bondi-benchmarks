"""Exercise the example without requiring Docker or the optional Yanex dependency."""

import runpy
import sys
from pathlib import Path
from unittest.mock import Mock

import pytest
from bondi import deployment

from bondi_benchmarks import ycsb


@pytest.mark.parametrize("backend", ["mongodb", "couchbase"])
@pytest.mark.parametrize("fail", [False, True])
def test_disposable_deployment(tmp_path, monkeypatch, backend, fail):
    params = {
        "backend": backend,
        "database": "lab",
        "version": "1.2.3",
        "workload": {"profile": "B", "record_count": 10, "operation_count": 10},
    }
    tracker = Mock()
    tracker.get_params.return_value = params
    tracker.get_experiment_id.return_value = "abcd1234"
    tracker.get_artifacts_dir.return_value = tmp_path
    monkeypatch.setitem(sys.modules, "yanex", tracker)
    deploy = Mock()
    target = deploy.return_value
    monkeypatch.setattr(deployment, f"deploy_{backend}", deploy)
    factory = Mock()
    monkeypatch.setattr(ycsb.YCSB, "from_deployment", factory)
    main = runpy.run_path(str(Path(__file__).resolve().parents[1] / "experiments/run_ycsb.py"))[
        "main"
    ]

    if fail:
        factory.return_value.run.side_effect = RuntimeError("benchmark failure")
        with pytest.raises(RuntimeError, match="benchmark failure"):
            main()
    else:
        main()
        assert tracker.log_metrics.call_count == 2

    assert deploy.call_args.args == (f"ycsb-{backend}-abcd1234",)
    assert deploy.call_args.kwargs["version"] == "1.2.3"
    if backend == "couchbase":
        assert deploy.call_args.kwargs["bucket"] == "lab"
    factory.return_value.load.assert_called_once()
    target.remove.assert_called_once_with()


def test_standalone_uses_fallback_id(monkeypatch):
    tracker = Mock()
    tracker.get_experiment_id.return_value = None
    monkeypatch.setitem(sys.modules, "yanex", tracker)
    deploy = Mock()
    monkeypatch.setattr(deployment, "deploy_mongodb", deploy)
    factory = Mock()
    monkeypatch.setattr(ycsb.YCSB, "from_deployment", factory)
    main = runpy.run_path(str(Path(__file__).resolve().parents[1] / "experiments/run_ycsb.py"))[
        "main"
    ]
    main()
    first = deploy.call_args.args[0]
    suffix = first.removeprefix("ycsb-mongodb-")
    assert len(suffix) == 8 and int(suffix, 16) >= 0
    assert factory.call_args.kwargs["artifact_dir"] == Path("artifacts") / suffix
    main()
    assert deploy.call_args.args[0] != first
    assert deploy.return_value.remove.call_count == 2
