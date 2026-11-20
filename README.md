# bondi-benchmarks

Run the Java Yahoo! Cloud Serving Benchmark (YCSB) against MongoDB or Couchbase
from Python. The package controls a Docker client and interprets measurements.
The example Yanex experiment records one load phase and one measured run.

## Quick start

From the repository root:

```sh
uv sync --locked --all-extras
cd experiments
uv run yanex run run_ycsb.py -p backend=mongodb
```

Docker downloads the matching published runner on first use. For an unreleased
checkout, see the [local build instructions](docs/installation.md).

## Project guide

| Path | Purpose |
| --- | --- |
| [Installation](docs/installation.md) | Set up Python dependencies and the Docker runner |
| [Python API guide](docs/ycsb.md) | Configure workloads and database connections |
| [Experiment guide](docs/experiments.md) | Run and compare tracked experiments |
| [src/bondi_benchmarks](src/bondi_benchmarks/) | Benchmark runner and results |
| [experiments](experiments/) | Yanex script and YAML configuration |
| [runner](runner/) | Pinned Java runner build |
| [notebooks](notebooks/) | Inspect saved measurements |
| [tests](tests/) | Package and documentation configuration checks |

## License

[MIT](LICENSE).
