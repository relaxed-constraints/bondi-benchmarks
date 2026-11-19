# Adding functionality

All examples refer to the original names of the starter project. If you've renamed it (see [Renaming the project](renaming.md)), use your new names instead.

## Python package

!!! tip "Package structure"
    This repository is structured as a Python package, where all core functionality resides under `src/empty_project/`. Consumers of this functionality include the command-line interface, the unit tests, Yanex experiment scripts, the Jupyter notebooks, and any other code that imports the package. By keeping your code organised in this way, you ensure that it is reusable, testable, and easy to maintain.

Add reusable functions and classes to modules under `src/`.
The starter function is `hello_world()` in `src/empty_project/hello.py`.

Add tests under `tests/`.
The file `tests/test_hello.py` contains tests for the `hello_world()` function in the `hello.py` module.

## Command-line interface

The file `src/empty_project/_cli.py` defines the command.
It uses [`argparse`](https://docs.python.org/3/library/argparse.html) to read arguments and calls the greeting function.

Add arguments here and keep reusable logic in package modules.

```sh
empty-cli --name World
empty-cli --help
```


## Experiments

!!! tip "Yanex experiment tracking"

    [Yanex](https://relaxed-constraints.github.io/yanex/) is a tool for running and managing experiments, logging results and artifacts. It allows you to define parameters, configurations, and metrics in a structured way.

Keep experiment scripts under `experiments/` and their YAML configurations under `experiments/configs/`. Don't add core functionality in experiment scripts, instead import reusable functions from your package.

Run an experiment from `experiments/`:

```sh
cd experiments
yanex run greet.py -c configs/config.yaml
yanex run greet.py -c configs/config.yaml -p name=Student # override the name parameter
```

The script prints a greeting and logs its length as a metric with Yanex.


## Notebooks

Open `notebooks/hello.ipynb` in VS Code with the Jupyter extension.
Select your project environment as the kernel.
The notebook calls the greeting function and plots a table with pandas and Matplotlib.

Use notebooks to explore data and analyse experiment results.
Move reusable functions into your package, including common data processing and plots.

## Check your changes

Run these commands from the repository root:

```sh
pytest
ruff check .
ruff format --check .
```

Continue with [Documentation changes](documentation.md).
