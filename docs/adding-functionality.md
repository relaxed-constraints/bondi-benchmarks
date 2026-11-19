# Adding functionality

## Python package

Add reusable functions and classes to modules under `src/`.
The starter function is `hello_world()` in `src/empty_project/hello.py`.
Use your renamed package directory after [Renaming the project](renaming.md).

Add tests under `tests/`.
The file `tests/test_hello.py` shows how to check printed output.

## Command-line interface

The file `src/empty_project/_cli.py` defines the command.
It uses `argparse` to read arguments and calls the greeting function.
Add arguments here and keep reusable logic in package modules.

Before renaming, run:

```sh
empty-cli --name World
empty-cli --help
```

Use your new command after renaming.

## Experiments

Keep experiment scripts under `experiments/`.
Keep their YAML configurations under `experiments/configs/`.
Import reusable functions from your package.

Run the starter experiment from `experiments/`:

```sh
cd experiments
yanex run greet.py -c configs/config.yaml
yanex run greet.py -c configs/config.yaml -p name=Student
```

The script prints a greeting and records the `name_length` metric.
Replace the greeting, parameters, and metric with your experiment logic.

## Notebooks

Open `notebooks/hello.ipynb` in VS Code with the Jupyter extension.
Select your project environment as the kernel.
The notebook calls the greeting function and plots a table with pandas and Matplotlib.

Use notebooks to explore data and experiment results.
Move reusable functions into your package.

## Check your changes

Run these commands from the repository root:

```sh
pytest
ruff check .
ruff format --check .
```

Continue with [Documentation changes](documentation.md).
