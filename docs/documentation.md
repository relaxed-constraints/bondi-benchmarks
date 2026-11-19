# Documentation changes

The site uses Zensical with shared defaults from relcon-docs.
Edit `mkdocs.yml` for project settings and navigation.

## Write project pages

1. Replace `docs/index.md` with your project introduction.
2. Write task instructions and examples in the [User guide](user-guide.md).
3. Add pages under `docs/` as needed.
4. Add each page to `nav` in `mkdocs.yml`.
5. Replace the starter Getting started pages with installation and setup steps for your users.

Use one `#` title per page.
Use `##` headings for sections.
Use relative links between pages.

Markdown supports code blocks, tables, callouts, Mermaid diagrams, and equations.
See the [presentation template](progress/template/presentation.md) for examples.

## Update the API reference

The file `docs/api-reference.md` displays Python modules with mkdocstrings:

```markdown
::: empty_project.hello
```

Replace the module path after renaming.
Add entries for new public modules.

Write Google-style docstrings in the Python source.
Use `Args:`, `Returns:`, and `Raises:` to describe parameters, return values, and exceptions.
The API reference displays these descriptions.

## Preview and build

The [installation steps](installation.md#install-dependencies) include the documentation tools.
Preview the site from the active environment:

```sh
zensical serve
```

Open the local URL printed by the command.
Check the site before you commit:

```sh
relcon-docs configure --check
zensical build --strict
```

The build writes the site to `site/`.

## Publish

Use the repository and site settings from [Renaming the project](renaming.md#update-project-information).
In your GitHub repository, select **Settings → Pages → Build and deployment → Source → GitHub Actions**.

Commit your changes and push to `main`.
The Documentation workflow runs checks before it publishes the site.
Open the **Actions** tab to check the result.
You can also start the Documentation workflow manually.

## Update shared defaults

Keep generated files in `.relcon-docs/`, `docs/stylesheets/`, `docs/javascripts/`, and `docs/overrides/` unchanged.
Put custom settings in `mkdocs.yml` or a separate stylesheet.

To upgrade relcon-docs, update its version in `pyproject.toml`.
Then run:

```sh
uv sync --group docs
relcon-docs configure --dry-run
relcon-docs configure
relcon-docs configure --check
zensical build --strict
```

Continue with [Progress updates](progress-updates.md).
