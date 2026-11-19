# Progress updates

Use progress pages to discuss your work with supervisors and collaborators.

1. Read the [presentation example](progress/example/) for Markdown examples.
2. Write your first update in `docs/progress/week-1/index.md`.
3. Include your question, progress, results, blockers, and next steps.
4. Keep figures beside the page, e.g. inside the `week-1` folder.

Separate presentation sections with `---` followed by a heading.
The file `docs/progress/.meta.yml` enables presentation mode for these pages.

Preview the site with `zensical serve`.
Open your update under **Progress**.
Select **Presentation mode** in a desktop-width window.
Use the arrow controls or Left/Right keys to move between sections.
Press **Esc** to exit.

## Adding sections to the Progress tab

To add a new section for a different week:

1. Create a new folder under `docs/progress/`, e.g. `week-2`.
2. Inside the new folder, create an `index.md` file for the weekly update.
3. Add the new week to the Progress section of `nav` in `mkdocs.yml`.