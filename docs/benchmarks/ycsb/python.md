# Run YCSB from Python

Both examples load 1,000 records into MongoDB and run 5,000 reads with YCSB profile C.

## From a BONDI deployment

Start MongoDB with BONDI. Pass the deployment to YCSB. BONDI supplies the connection details.

```python
from bondi.deployment import deploy_mongodb
from bondi_benchmarks import ycsb

deployment = deploy_mongodb("ycsb-mongo", port=27029)
try:
    benchmark = ycsb.YCSB.from_deployment(deployment, database="ycsb_lab")
    workload = ycsb.Workload("C", record_count=1000, operation_count=5000, threads=4)

    benchmark.load(workload)
    result = benchmark.run(workload)
    print(result.throughput_ops_s, "operations per second")
finally:
    deployment.remove()  # Remove the example deployment and its data.
```

## From an existing connection

Use a dedicated database. If `usertable` already exists, it must contain no documents.
MongoDB creates the collection on the first insert if it does not exist.

This example assumes MongoDB runs directly on the host machine and listens on port 27017.
Python connects to `localhost`. Inside the YCSB container, `localhost` refers to the container itself.
The example uses Docker Desktop’s `host.docker.internal` address so the container can reach MongoDB on the host.

```python
from bondi import MongoConnection
from bondi_benchmarks import ycsb

connection = MongoConnection("mongodb://localhost:27017")
benchmark = ycsb.YCSB.from_connection(
    connection,
    database="ycsb_lab",
    runner_endpoint="mongodb://host.docker.internal:27017",
)
workload = ycsb.Workload("C", record_count=1000, operation_count=5000, threads=4)

benchmark.load(workload)
result = benchmark.run(workload)
print(result.throughput_ops_s, "operations per second")
```

If the connection address works from both Python and the container, omit `runner_endpoint`.
