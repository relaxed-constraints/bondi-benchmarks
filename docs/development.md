# Contributor guide

Run these commands from the repository root. Install the development dependencies first.

```sh
uv sync --locked --all-extras --group docs
```

## Test and format the code

Run the tests, check the lint rules, and check the format.

```sh
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

To apply formatting changes, run `uv run ruff format .`.

## Build and preview the documentation

Check the shared configuration. Build the site with strict checks.

```sh
uv run relcon-docs configure --check
uv run zensical build --strict
```

Start the preview server. Open the local address that the server prints.

```sh
uv run zensical serve
```

## Build the YCSB runner

Build a local image. Use the image for a tracked experiment.

```sh
docker build -t bondi-ycsb:dev runners/ycsb
cd experiments/ycsb
uv run yanex run benchmark.py -c configs/default.yaml -p runner_image=bondi-ycsb:dev
```

The Python factories accept the same reference via `image="bondi-ycsb:dev"`.

## Publish the YCSB runner

Publishing a GitHub Release for a tag matching the package version (for example
`v0.1.0`) builds a Linux amd64/arm64 image and publishes it under the version
tag (`0.1.0`). Main-branch pushes run the usual CI. To publish on demand, run
**Publish YCSB runner** from Actions. Selecting a branch publishes a preview
tagged `sha-<full-commit-sha>`. Selecting the matching Git tag publishes the
package-version image. The workflow prints the published reference and digest.
After the first publication, set the GHCR package visibility to **Public** so
students can pull anonymously.

The build downloads checksum-pinned upstream YCSB commit `ae02b31fa7784b3892f121c06638aa0cd972fa06`. It uses the synchronous
MongoDB driver 5.1.0 and Couchbase Java SDK 2.7.23. Two small build patches
omit the unused legacy async MongoDB dependency and enable Couchbase RBAC.
The benchmark workload and measurement code come from upstream.
