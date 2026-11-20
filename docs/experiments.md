# Yanex experiments

With the virtual environment active and the working directory set to `experiments/`:

```sh
yanex run run_ycsb.py -c configs/ycsb.yaml -p backend=mongodb
```

Each experiment creates a fresh BONDI deployment named `ycsb-<backend>-<yanex-id>`,
loads the data,
runs YCSB, and removes the deployment and its data volume when the benchmark
finishes or raises an exception. Yanex retains metrics and artifacts. Set
`backend` to `mongodb` or `couchbase` and optionally set a full server version:

```sh
yanex run run_ycsb.py -p backend=couchbase -p version=7.6.2
```

For a standalone run, execute `python run_ycsb.py` from `experiments/`. The
script reads `configs/ycsb.yaml`, generates a unique ID for the deployment,
and saves phase artifacts under `./artifacts/<id>/`. Yanex tracks metrics
only when invoked through its runner. Both modes remove the deployment afterward.

From `experiments/`, Yanex automatically loads `config.yaml`, which links to
`configs/ycsb.yaml`. CLI overrides are applied to these defaults.

Omitting the version selects BONDI's default. BONDI creates the requested
Couchbase bucket during startup. Use free host ports from the example config
and run experiments that share ports sequentially.

Each phase saves a versioned result, diagnostic streams, and flat metrics such as
`run_read_p99_us` and `run_throughput_ops_s`. Different phases share Yanex step zero.
A failed YCSB phase preserves diagnostic output and marks the experiment failed.
Use `result.metrics()` or `result.to_dict()` directly in other experiment frameworks.
For a read-only repeat against the same data, reuse `benchmark.run(workload)` in Python.
Run one benchmark at a time on each host when comparing results.

Pass `artifact_dir=path` to the runner to keep all YCSB output under a directory
of your choice. The tracked experiment passes `yanex.get_artifacts_dir()`. Each phase gets a fresh load- or run-
prefixed subdirectory with stdout.txt, stderr.txt and result.json on success.
Failed benchmark measurements retain both streams and an error.txt diagnostic.
