# Git and GitHub workflow

Use a feature branch for each change.
Keep each pull request (PR) focused and reasonably small.
Limit each PR to one week of work at most.

## Create a feature branch

Start from an updated `main` branch:

```sh
git switch main
git pull
git switch -c my-new-feature
```

## Make changes

Implement your change.
Add or update tests for the changed behaviour.
Update the documentation and docstrings to match the code.

## Run checks

Run these commands from the repository root with the project environment active:

```sh
ruff format .
pytest
ruff check .
ruff format --check .
zensical build --strict
```

Fix any errors before you commit.

## Commit on your branch

Check the changed files, then commit:

```sh
git status
git add .
git commit -m "Describe your change"
```

Repeat these steps as you work.

## Push and create a PR

When the change is ready for review, push your branch:

```sh
git push -u origin my-new-feature
```

Open your repository on GitHub.
Create a pull request from `my-new-feature` into `main`.
Describe the change and how you checked it.

## Review and merge

Ask another person or an AI integration to review your code.
Address the review comments.
Run the checks again after changes.
Commit and push the updates to the same branch.
The PR updates automatically.

Once the review is complete and GitHub checks pass, merge the PR into `main`.

## Update your local copy

After the merge, return to `main` and delete your local feature branch:

```sh
git switch main
git pull
git branch -d my-new-feature
```

Create a new branch for the next change and repeat this workflow.

Continue with [Adding functionality](adding-functionality.md).
