"""Provision a BONDI deployment, prepare its dataset, and track a YCSB run."""

from pathlib import Path
from uuid import uuid4

import yaml
import yanex
from bondi.deployment import deploy_couchbase, deploy_mongodb

from bondi_benchmarks import ycsb


def main():
    run_id = yanex.get_experiment_id()
    if run_id is None:
        run_id = uuid4().hex[:8]
        config = Path(__file__).parent / "configs" / "ycsb.yaml"
        params = yaml.safe_load(config.read_text())
        artifact_dir = Path("artifacts") / run_id
    else:
        params = yanex.get_params()
        artifact_dir = yanex.get_artifacts_dir()
    backend = params.get("backend", "mongodb")
    if backend not in {"mongodb", "couchbase"}:
        raise ValueError("backend must be mongodb or couchbase")
    version = params.get("version", None)
    name = f"ycsb-{backend}-{run_id}"
    database = params.get("database")
    if not isinstance(params.get("workload"), dict) or not database:
        raise ValueError(
            "A database and workload mapping are required. From experiments/, "
            "run yanex run run_ycsb.py -c configs/ycsb.yaml -p backend=couchbase"
        )
    workload = ycsb.Workload(**params["workload"])
    print(f"Starting deployment {name}", flush=True)
    if backend == "mongodb":
        target = deploy_mongodb(name, version=version, port=params.get("mongodb_port", 27029))
    else:
        target = deploy_couchbase(
            name,
            version=version,
            bucket=database,
            management_port=params.get("management_port", 18091),
            query_port=params.get("query_port", 18093),
            kv_port=params.get("kv_port", 21210),
        )

    try:
        benchmark = ycsb.YCSB.from_deployment(target, database, artifact_dir=artifact_dir)
        print(f"Loading data into {database}", flush=True)
        loaded = benchmark.load(workload)
        yanex.log_metrics(loaded.metrics(), step=0)

        print(
            f"Running YCSB workload {workload.profile} "
            f"({workload.record_count:,} records, {workload.operation_count:,} operations, "
            f"{workload.threads:,} threads)",
            flush=True,
        )
        result = benchmark.run(workload)
        yanex.log_metrics(result.metrics(), step=0)
    finally:
        print(f"Removing deployment {name}", flush=True)
        target.remove()


if __name__ == "__main__":
    main()
