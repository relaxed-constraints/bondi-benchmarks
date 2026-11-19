# Renaming the project

This example uses three names:

| Name | Example | Purpose |
| --- | --- | --- |
| Project | `my-project` | Repository and Python distribution |
| Package | `my_project` | Python imports and source directory |
| Command | `my-cli` | Command-line interface |

Use your own names in the steps below.
Use underscores in the Python package name.

## Rename the package and command

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

3. Replace `empty_project` with `my_project` in these files:

   - `src/my_project/_cli.py`
   - `experiments/greet.py`
   - `notebooks/hello.ipynb`
   - `tests/test_hello.py`
   - `docs/api-reference.md`

## Update project information

| File | Changes |
| --- | --- |
| `README.md` | Update the title, introduction, links, and repository structure. |
| `mkdocs.yml` | Update `site_name`, `site_description`, `site_url`, `repo_url`, `repo_name`, and `copyright`. |
| `docs/index.md` | Describe your research question and project goals. |
| `docs/installation.md` | Replace the starter clone URL and directory with your repository. Use your new command in the installation check. |
| Other pages under `docs/` | Replace starter names, commands, and examples with your project content. |
| `LICENSE` | Add your copyright notice. Keep the existing MIT notice. |
| `CHANGELOG.md` | Replace the starter history with changes for your project. |

Use `https://YOUR-ACCOUNT.github.io/my-project/` as `site_url` for a GitHub Pages project site.
Keep the trailing slash.
Use your repository URL for `repo_url` and `YOUR-ACCOUNT/my-project` for `repo_name`.

Keep references to BONDI, Yanex, and relcon-docs where your project uses those tools.

## Connect your repository

Create an empty repository under your GitHub account or organisation.
Add its URL as the new remote:

```sh
git remote add origin https://github.com/YOUR-ACCOUNT/my-project.git
git remote -v
```

Check that both URLs point to your repository.

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

Check the renamed command and project:

```sh
my-cli --name World
pytest
ruff check .
ruff format --check .
zensical build --strict
```

Search the tracked files for names you missed:

```sh
git grep -n -e empty_project -e empty-cli -e bondi-empty-project
```

Review each match, including examples on this page.
Continue with [Adding functionality](adding-functionality.md).
