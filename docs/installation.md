# Installation

Use Python 3.11+, a local Docker engine, and the current BONDI checkout at `../bondi`. From this checkout:

```sh
uv sync --extra yanex --extra couchbase
docker build -t bondi-benchmarks/ycsb:ae02b31-1 runner
```

The build downloads checksum-pinned upstream YCSB commit `ae02b31fa7784b3892f121c06638aa0cd972fa06`. It uses the synchronous
MongoDB driver 5.1.0 and Couchbase Java SDK 2.7.23. Two small build patches
omit the unused legacy async MongoDB dependency and enable Couchbase RBAC.
The benchmark workload and measurement code come from upstream. Runner images
are local; each result records the exact image ID.

For development checks, install the documentation dependencies with `uv sync --locked --all-extras --group docs`.
