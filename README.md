# BONDI empty project

A minimal starting point for students building their own BONDI research project.
It uses the same dependencies as [bondi-demo-project](https://github.com/relaxed-constraints/bondi-demo-project), 
but starts with a barebones setup with one reusable function and examples of calling it from an experiment, a notebook and a test.

See [Dependencies](docs/dependencies.md) for the libraries and tools used in this project.

## Repository structure

| Directory | Purpose |
| --- | --- |
| `docs/` | Space for project notes and instructions. |
| `experiments/` | Yanex scripts; `greet.py` calls the greeting helper and logs a metric. |
| `experiments/configs/` | YAML parameters; `config.yaml` contains `name`. |
| `notebooks/` | Examples calling the helper and plotting a small table with pandas and Matplotlib. |
| `docs/progress/` | Progress updates and a reusable presentation template. |
| `src/empty_project/` | Reusable Python code goes here, replacing the `hello.py` stub. |
| `tests/` | A unit test checking the greeting printed by `hello_world()`. |


## Getting started

Start with [Installation](docs/installation.md).
Follow the [rename checklist](docs/renaming.md) to make the project your own.

- [Adding functionality](docs/adding-functionality.md)
- [Documentation changes](docs/documentation.md)
- [Progress updates](docs/progress-updates.md)

## License

[MIT](LICENSE).
