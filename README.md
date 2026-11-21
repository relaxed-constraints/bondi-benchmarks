# BONDI Benchmarks

BONDI Benchmarks provides Python tools and Yanex experiments for database benchmarks.

## Available benchmarks

The Yahoo! Cloud Serving Benchmark (YCSB) measures throughput and latency for database operations.
The runner supports MongoDB and Couchbase.

1. [Install the project](docs/installation.md).
2. [Run the Yanex experiment](docs/benchmarks/ycsb/experiments.md).
3. [Interpret the results](docs/benchmarks/ycsb/results.md).

Use the [Python guide](docs/benchmarks/ycsb/python.md) to run YCSB against an existing database.

## Repository layout

Each benchmark uses the same directory name across the repository.

| Directory | Contents |
| --- | --- |
| `src/bondi_benchmarks/<benchmark>/` | Python API and result types |
| `experiments/<benchmark>/` | Yanex scripts and configurations |
| `runners/<benchmark>/` | Docker build files |
| `notebooks/<benchmark>/` | Analysis notebooks |
| `tests/<benchmark>/` | Benchmark tests |
| `docs/benchmarks/<benchmark>/` | User guides |
| `docs/api/<benchmark>.md` | API reference |

## License

[MIT](LICENSE).
