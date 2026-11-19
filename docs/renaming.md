# Renaming the project

This page walks you through all the steps to rename the project to your own name.

This example uses three names:

| Component | New Name | Purpose |
| --- | --- | --- |
| Project | `my-project` | Repository and Python distribution |
| Package | `my_project` | Python imports and source directory |
| Command | `my-cli` | Command-line interface |

Use your own names in the steps below. Use underscores in the Python package name.

## Rename the package and CLI command

1. Rename `src/empty_project/` to `src/my_project/`.
2. Update these entries in `pyproject.toml`:
   ```toml
   [project]
   name = "my-project"
   authors = [{ name = "Your Name", email = "you@example.com" }]
   version = "0.1.0"
   description = "Your project description"

   [project.scripts]
   my-cli = "my_project._cli:main"

   [tool.hatch.build.targets.wheel]
   packages = ["src/my_project"]
   ```
   Keep the other fields and sections.
   Review `dependencies` and `requires-python` for your project.
3. Replace the package name `empty_project` with `my_project` in these files:

     - `src/my_project/_cli.py`
     - `experiments/greet.py`
     - `notebooks/hello.ipynb`
     - `tests/test_hello.py`
     - `docs/api-reference.md`

## Update project information

| File | Changes |
| --- | --- |
| `README.md` | Update the title, introduction, links, and repository structure. |
| `mkdocs.yml` | Documentation config file. Update `site_name`, `site_description`, `site_url`, `repo_url`, `repo_name`, and `copyright`. |
| `docs/installation.md` | Replace this file with your own installation instructions |
| Other pages under `docs/` | Replace with your project content. |
| `LICENSE` | Add your copyright notice. Keep the existing MIT notice. |
| `CHANGELOG.md` | Replace the starter history with changes for your project. |

Use `https://YOUR-ACCOUNT.github.io/my-project/` as `site_url` for a GitHub Pages project site.
Keep the trailing slash.
Use your repository URL for `repo_url` and `YOUR-ACCOUNT/my-project` for `repo_name`.

## Connect your Github repository

Create an empty repository under your GitHub account or organisation.
Add its URL as the new remote:

```sh
git remote add origin https://github.com/YOUR-ACCOUNT/my-project.git
git remote -v
```

This command prints two URLs. Check that both URLs point to your repository.

## Reinstall and check

Install the renamed package in your project environment:

=== "uv"

    Refresh `uv.lock` and reinstall:

    ```sh
    uv sync --group docs
    ```

=== "pip"

    ```sh
    python -m pip install -e . --group dev --group docs
    ```

Check that everything still works, including tests (`pytest`), linting and formatting (`ruff`) and the documentation build (`zensical`):

```sh
my-cli --name World
pytest
ruff check .
ruff format --check .
zensical build --strict
```

Finally, search the tracked files for names you may have missed:

```sh
git grep -n -e empty_project -e empty-cli -e bondi-empty-project
```

Review each match, including examples on this page.
Continue with [Adding functionality](adding-functionality.md).
