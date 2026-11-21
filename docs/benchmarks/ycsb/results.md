# Interpret YCSB results

YCSB measures throughput for the whole workload and latency for each operation type.
The Python runner returns these measurements, operation counts, and status counts for each phase.

YCSB has six workload profiles. Profile C reads records. Profile B mixes reads and updates.
See the [YCSB core workloads guide](https://github.com/brianfrankcooper/YCSB/wiki/Core-Workloads) for the operation mix and use case for each profile.

## Read a result in Python

After you load the data, run the profile C workload from the [Python guide](python.md).

```python
result = benchmark.run(workload)
metrics = result.metrics()
print("Operations per second:", metrics["run_throughput_ops_s"])
print("99th percentile read latency (µs):", metrics["run_read_p99_us"])

record = result.to_dict()
print("Completed reads:", record["operations"]["READ"]["count"])
```

Each phase returns a `ycsb.Result`. Use `metrics()` for flat metrics or `to_dict()` for the versioned result.
For example, `run_read_p99_us` gives the 99th percentile of read latency in microseconds.
The metric `run_throughput_ops_s` gives operations per second.

See the [Result API reference](../../api/ycsb.md#bondi_benchmarks.ycsb.Result) for all fields and methods.

## Load results with Yanex

The [Yanex experiment](experiments.md) records metrics for the load and run phases.
Replace the example ID with the ID that Yanex printed for your run.

```python
import yanex.results as yr

metrics = yr.get_metrics(
    ids=["67620075"],
    metrics=["run_throughput_ops_s", "run_read_p99_us"],
    params="none",
)
print(metrics[["metric_name", "value"]])
```

## Compare backends

Use freshly loaded data for each backend. Run one benchmark at a time on each host.

Profile B reads and updates records. By default, YCSB sends one field for each update.
The Couchbase KV binding replaces the document with that field. MongoDB preserves the other fields.

For partial updates, set `couchbase.kv: false` to use SQL++ on Couchbase.
For full-record updates, set `writeallfields: true` on both backends.
Record the settings with the results.
