# Installation

Install Python 3.11 or later. Start Docker. Clone the repository and enter its root directory.

```sh
git clone https://github.com/relaxed-constraints/bondi-benchmarks.git
cd bondi-benchmarks
```

Select one installation method. The base package includes Yanex and MongoDB support. The commands below also install the optional Couchbase support.

=== "uv"

    ```sh
    uv sync --locked --extra couchbase
    source .venv/bin/activate
    ```

=== "pip"

    ```sh
    python -m venv .venv
    source .venv/bin/activate
    python -m pip install --editable '.[couchbase]'
    ```

On the first YCSB run, Docker downloads `ghcr.io/relaxed-constraints/bondi-benchmarks/ycsb:0.1.0`
from GitHub Container Registry. The image includes Java and the YCSB bindings.
Later experiments use the local Docker cache. Each result records the image
reference and the local image ID used for execution.

Continue to the [Yanex experiment](benchmarks/ycsb/experiments.md).
