# Changelog

## Unreleased

- Update relcon-docs defaults and deployment workflow; inherit equation rendering,
  diagram accent colours and dark-mode Markdown copy controls.

- Use shared light/dark diagram colours from relcon-docs.

- Inherit callouts, collapsible notes and Mermaid support from relcon-docs.

- Inherit Markdown exports and llms.txt directly from relcon-docs, removing
  duplicate project-level export configuration.

- Adopt relcon-docs through a dedicated docs dependency group and inherited YAML
  configuration, retaining Mermaid styling and project-specific API headings.
- Enable Markdown exports and llms.txt, and reuse the shared Pages workflow
  while preserving push-to-main and manual deployment after CI succeeds.

- Add a Zensical documentation scaffold, API reference and GitHub workflows.
- Upgrade to BONDI 0.3.1 and Yanex 0.7.0.
- Update BONDI deployment commands to the current CLI.
