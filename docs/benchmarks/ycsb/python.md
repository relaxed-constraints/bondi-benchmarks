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

Use a dedicated database with an empty `usertable` collection. Python and the YCSB container must both reach the same MongoDB server.

This example uses Docker Desktop. Python connects to MongoDB on the host through `localhost`.
Inside the container, `localhost` refers to the container itself. Use `runner_endpoint` to give YCSB the host address.

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
