# Installation

Install Python 3.11 or newer and Git.
Install Docker with Compose v2 to run local databases.

## Copy the starter

Clone the repository into your project directory:

```sh
git clone https://github.com/relaxed-constraints/bondi-empty-project.git my-project
cd my-project
```

Remove the starter remote:

```sh
git remote remove origin
```

## Install dependencies

=== "uv"

    Install [uv](https://docs.astral.sh/uv/getting-started/installation/).

    ```sh
    uv sync --locked --group docs
    source .venv/bin/activate
    ```

=== "pip"

    ```sh
    python -m venv .venv
    source .venv/bin/activate
    python -m pip install --upgrade pip
    python -m pip install -e . --group dev --group docs
    ```

On Windows PowerShell, activate the environment with `.venv\Scripts\Activate.ps1`.
The following pages assume an active environment.
Run commands from the repository root unless a step specifies another directory.

## Check the installation

```sh
empty-cli --name World
pytest
```

The command prints `Hello, World`.
The tests do not need a database.

Continue with [Renaming the project](renaming.md).
