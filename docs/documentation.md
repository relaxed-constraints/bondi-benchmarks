# Documentation changes

The site uses [Zensical](https://zensical.org/) to produce the project documentation from Markdown files. Edit `mkdocs.yml` for project settings and navigation.

To start the documentation server locally, run `zensical serve` in your project directory, see [Preview changes locally](#preview-changes-locally) below.

## Write project pages

1. Replace `docs/index.md` with your project introduction.
2. Write task instructions and examples on pages under the User guide section.
3. Add pages under `docs/` as needed.
4. Add each page to `nav` in `mkdocs.yml`.
5. Replace the starter User guide pages with instructions for your users.

Use one `#` title per page.
Use `##` headings for sections.
Use relative links between pages.

Markdown supports code blocks, tables, callouts, Mermaid diagrams, and equations.
See the [presentation example](progress/example/) for examples.

## Update the API reference

The file `docs/api-reference.md` displays Python modules with mkdocstrings:

```markdown
::: empty_project.hello
```

Replace the module path after renaming.
Add entries for new public modules.

Write Google-style docstrings in the Python source.
Use `Args:`, `Returns:`, and `Raises:` to describe parameters, return values, and exceptions.
The API reference displays these descriptions automatically.

## Preview changes locally

To preview your changes locally, start the local documentation server with:

```sh
zensical serve
```

Then open your browser and navigate to `http://localhost:8000` to preview the documentation.

If the port is taken, specify another port with:

```sh
zensical serve --dev-addr localhost:8001
```


## Publish your documentation

If you want your documentation to be publicly available using Github Pages, follow these steps.

In your GitHub repository, select **Settings → Pages → Build and deployment → Source → GitHub Actions**.

Commit your changes, merge the feature branch to `main` and push to GitHub, or merge a pull request from the GitHub interface. This automatically triggers the documentation workflow and deploys your site to your GitHub Pages under `https://<your-username>.github.io/<your-repository>/`.

You can also start the documentation workflow manually under the **Actions** tab in your GitHub repository.


Continue with [Progress updates](progress-updates.md).
