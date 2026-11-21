# Run YCSB with Yanex

Activate the project environment. From the repository root, enter the experiment directory.

```sh
cd experiments/ycsb
```

```sh
yanex run benchmark.py -c configs/default.yaml
```

The default experiment uses MongoDB and profile C. To select Couchbase and a database version, use this command.

```sh
yanex run benchmark.py -c configs/default.yaml -p backend=couchbase -p version=7.6.2
```

1. The script creates a deployment named `ycsb-<backend>-<yanex-id>`.
2. YCSB loads records into the database.
3. YCSB runs the workload. Yanex records metrics from both phases at step zero.
4. The script removes the deployment and its volume, including after a benchmark error.

Omit the version to use the BONDI default. BONDI creates the Couchbase bucket during startup.
Select free host ports in the configuration. Run experiments that share ports one at a time.

For a standalone run, use `python benchmark.py`. The script reads its default configuration.
It creates a unique identifier and saves artifacts in `./artifacts/<id>/`.
Use the Yanex command to track metrics across runs.
