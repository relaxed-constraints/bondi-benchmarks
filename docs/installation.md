# Installation

Use Python 3.11+, a local Docker engine, and the current BONDI checkout at `../bondi`. From this checkout:

```sh
uv sync --extra yanex --extra couchbase
```

On first use the runner pulls `ghcr.io/relaxed-constraints/bondi-benchmarks/ycsb:<package-version>`
from GitHub Container Registry. The image includes Java and the YCSB bindings.
Later experiments use the local Docker cache. Each result records the image
reference and the local image ID used for execution.

For an unreleased checkout you can build locally and select the image explicitly:

```sh
docker build -t bondi-ycsb:dev runner
cd experiments
uv run yanex run run_ycsb.py -p runner_image=bondi-ycsb:dev
```

The Python factories accept the same reference via `image="bondi-ycsb:dev"`.

## Publishing the runner

Publishing a GitHub Release for a tag matching the package version (for example
`v0.1.0`) builds a Linux amd64/arm64 image and publishes it under the version
tag (`0.1.0`). Main-branch pushes run the usual CI. To publish on demand, run
**Publish YCSB runner** from Actions. Selecting a branch publishes a preview
tagged `sha-<full-commit-sha>`; selecting the matching Git tag publishes the
package-version image. The workflow prints the published reference and digest.
After the first publication, set the GHCR package visibility to **Public** so
students can pull anonymously.

The build downloads checksum-pinned upstream YCSB commit `ae02b31fa7784b3892f121c06638aa0cd972fa06`. It uses the synchronous
MongoDB driver 5.1.0 and Couchbase Java SDK 2.7.23. Two small build patches
omit the unused legacy async MongoDB dependency and enable Couchbase RBAC.
The benchmark workload and measurement code come from upstream.

For development checks, install the documentation dependencies with `uv sync --locked --all-extras --group docs`.
