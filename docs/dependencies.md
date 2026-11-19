# Dependencies

This project uses the following libraries and tools.

## uv

If you're unfamiliar with `uv`, it's worth spending some time to understand its
role in managing virtual environments, dependencies, publishing packages and
running scripts. `uv` is a modern tool for Python project management that
simplifies these tasks compared to traditional approaches using `virtualenv`,
`pip`, and custom shell scripts.

You don't need to use `uv` and can install the dependencies with `pip`, but using
`uv` simplifies managing the project environment and dependencies.

Read about `uv` features in the [official documentation](https://docs.astral.sh/uv/getting-started/features/).

## pytest

pytest is a framework for writing and running Python tests.
Run the tests in this project with `pytest`.

Read more in the [pytest documentation](https://docs.pytest.org/en/stable/).

## Ruff

Ruff checks and formats Python code.
This project uses it to find code errors, check imports, and keep formatting consistent.
Run it with

```sh
ruff check
ruff format --check
```

Read more in the [Ruff documentation](https://docs.astral.sh/ruff/).

## pandas

pandas provides DataFrames: tables that you can filter, group and summarise in
Python. They are great for experiment analysis and data manipulation and work
well together with Matplotlib and Jupyter notebooks.

Read more in the [pandas documentation](https://pandas.pydata.org/docs/).

## Matplotlib

Matplotlib creates plots from Python data. We use it with pandas to generate charts and visualise
experiment results.

Read more in the [Matplotlib documentation](https://matplotlib.org/stable/users/index.html).


## Jupyter Notebooks

Jupyter notebooks combine executable code, explanations and plots in one document.
We use them to explore saved experiment results interactively. Open the notebooks
in VS Code with its Jupyter extension and select this project's Python environment
as the kernel that runs the code.

Read more in the [Jupyter documentation](https://docs.jupyter.org/en/latest/).


## Zensical

Zensical builds documentation websites from Markdown files.
This project uses it to preview and publish its documentation.

Read more in the [Zensical documentation](https://zensical.org/docs/).

## BONDI

BONDI is a toolkit for conducting research with document databases, with a focus on MongoDB
and Couchbase. It provides tools for deploying databases, generating, running and profiling
query workloads, analysing the schema of database collections, and generating load on a
database for performance testing.

More info and the full documentation can be found on the [BONDI documentation site](https://relaxed-constraints.github.io/bondi/).


## Yanex

Yanex is a generic tool for managing experiments and tracking and analysing their results.
It allows you to run scripts with specific configurations, record the outputs, and maintain
a history of experiments. This is particularly useful for reproducibility and for
understanding the impact of different parameters on your results.

More info can be found in the [Yanex documentation](https://relaxed-constraints.github.io/yanex/).
