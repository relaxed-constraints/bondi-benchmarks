"""Provision a BONDI deployment, prepare its dataset, and track a YCSB run."""

from pathlib import Path
from uuid import uuid4

import yaml
import yanex
from bondi.deployment import deploy_couchbase, deploy_mongodb

from bondi_benchmarks import ycsb


def main():
    if yanex.is_standalone():
        run_id = uuid4().hex[:8]
        config = Path(__file__).parent / "configs" / "default.yaml"
        params = yaml.safe_load(config.read_text())
        artifact_dir = Path("artifacts") / run_id
    else:
        run_id = yanex.get_experiment_id()
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
            "run yanex run ycsb/run.py -c ycsb/configs/default.yaml -p backend=couchbase"
        )

    workload = ycsb.Workload(**params["workload"])

    # deploy the database backend
    print(f"Starting deployment {name}", flush=True)
    if backend == "mongodb":
        deployment = deploy_mongodb(name, version=version, port=params.get("mongodb_port", 27029))
    else:
        deployment = deploy_couchbase(
            name,
            version=version,
            bucket=database,
            management_port=params.get("management_port", 18091),
            query_port=params.get("query_port", 18093),
            kv_port=params.get("kv_port", 21210),
        )

    try:
        # create benchmark and load data
        benchmark = ycsb.YCSB.from_deployment(
            deployment,
            database,
            image=params.get("runner_image", ycsb.IMAGE),
            artifact_dir=artifact_dir,
        )
        print(f"Loading data into {database}", flush=True)
        loaded = benchmark.load(workload)
        yanex.log_metrics(loaded.metrics(), step=0)

        # run the benchmark
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
        deployment.remove()


if __name__ == "__main__":
    main()
