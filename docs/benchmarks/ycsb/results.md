# Interpret YCSB results

Profile C reads records. Use freshly loaded data for each backend. Run one benchmark at a time on each host.

Profile B reads and updates records. By default, YCSB sends one field for each update.
The Couchbase KV binding replaces the document with that field. MongoDB preserves the other fields.

For partial updates, set `couchbase.kv: false` to use SQL++ on Couchbase.
For full-record updates, set `writeallfields: true` on both backends.
Record the settings with the results.

Each phase returns a `ycsb.Result`. Use `metrics()` for flat metrics or `to_dict()` for the versioned result.
For example, `run_read_p99_us` gives the 99th percentile of read latency in microseconds.
The metric `run_throughput_ops_s` gives operations per second.

The experiment saves each phase in a separate artifact directory.
Each successful phase includes `stdout.txt`, `stderr.txt`, and `result.json`.
A failed measurement retains both streams and an `error.txt` file.
In Python, pass `artifact_dir` to the factory to choose the parent directory.
Call `benchmark.run(workload)` again to repeat a read-only workload on the same data.
