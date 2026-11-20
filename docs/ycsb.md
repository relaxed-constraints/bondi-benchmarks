# YCSB Python API

```python
from bondi.deployment import deploy_mongodb
from bondi_benchmarks import ycsb

deployment = deploy_mongodb("ycsb-mongo", port=27029)
benchmark = ycsb.YCSB.from_deployment(deployment, database="ycsb_lab")
workload = ycsb.Workload("B", record_count=1000, operation_count=5000, threads=4)

loaded = benchmark.load(workload)
result = benchmark.run(workload)
print(result.throughput_ops_s, result.operations["READ"].p99_us)
```

For Couchbase, create a deployment with a dedicated bucket, for example
`deploy_couchbase("ycsb-couch", bucket="ycsb_lab")`, and pass that deployment
to `YCSB.from_deployment()`. Use free management, query and KV ports if running
other Couchbase deployments. The load checks MongoDB's `usertable` collection
or the Couchbase bucket's default collection for existing documents. Couchbase
requires a pre-existing bucket and a server supporting KV range scan for this check.
Use a dedicated destination with one writer. A failed load can leave partial data.
Choose a fresh destination before retrying. The package never resets the database.

For an existing database, pass a `MongoConnection` or `CouchbaseConnection` to
`benchmark = ycsb.YCSB.from_connection(connection, database="ycsb_lab")`.
This factory uses bridge networking. Inside the runner, localhost refers to the
runner itself. For a local BONDI deployment use `from_deployment(deployment, ...)`
to select the managed route automatically.
The Python connection must reach the target for the load check. The Docker runner
must reach that same database and its advertised addresses. For a host-local
MongoDB on Docker Desktop, pass `runner_endpoint="mongodb://host.docker.internal:27017"`
alongside the host connection. For a remote database, a routable URI usually works
directly. Managed deployments automatically share the database container's network
namespace. The runner accepts standard MongoDB URIs and DNS seed lists such as
`mongodb+srv://cluster.example.com/`. Both the host and runner must be able to
resolve the SRV records. The driver reads authentication options from DNS TXT
records unless the URI specifies them. If your SRV deployment uses database-specific
authentication without a TXT authSource, specify the authentication database with
`authSource` when the benchmark database differs from it.
Keep credentials on the connection object; endpoint overrides select the route.

Profiles A–F provide defaults. Pass native YCSB workload and binding properties
through the same mapping in Python or Yanex YAML. For example, use Couchbase's
query path for single-field updates:

```python
workload = ycsb.Workload(
    "B", 1000, 5000, properties={"writeallfields": False, "couchbase.kv": False}
)
```

```yaml
workload:
  profile: B
  record_count: 1000
  operation_count: 5000
  properties:
    writeallfields: false
    couchbase.kv: false
```

Use literal property names and scalar values. Both phases receive the properties;
native YCSB and the selected binding interpret them. The wrapper validates the
standard YCSB result format and completed operation counts, so options that change
the output format or terminate a phase early can produce a validation error.
Keep credentials on the connection: workload properties are saved in run artifacts.
Use the typed arguments for counts, threads and target rate, and the target object
for the database connection. Set `target_ops_s` to rate-limit the run and
`load(workload, threads=...)` to override load concurrency.
Workload E on Couchbase requires a suitable index and the Query service. Provision
the index separately. D and E add records, so account for initial state across repetitions.
