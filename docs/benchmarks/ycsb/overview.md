# YCSB overview

The [Yahoo! Cloud Serving Benchmark (YCSB)](https://github.com/brianfrankcooper/YCSB) measures how a database responds to a stream of requests.
For example, how quickly can a database retrieve user profiles while other clients update them?
With BONDI Benchmarks, you can run the same workload against MongoDB or Couchbase.

## How a run works

The **load phase** inserts records. Each record has a key and a set of fields.
The **run phase** sends requests against those records. The workload determines which operations to send and which records to access.

YCSB measures performance from the client. **Throughput** tells you how many operations finish per second across all client threads.
**Latency** tells you how long an operation takes. YCSB reports latency separately for reads, updates, and other operation types.
For example, a 99th percentile read latency of 2 milliseconds means about 99% of reads finished within 2 milliseconds.

## Workload profiles

The six core profiles represent different patterns of database use. The table gives the default mix for each profile.
See the [YCSB core workloads guide](https://github.com/brianfrankcooper/YCSB/wiki/Core-Workloads) and the [workload configuration files](https://github.com/brianfrankcooper/YCSB/tree/master/workloads) for details.

| Profile | Default operations | Example |
| --- | --- | --- |
| A | 50% reads, 50% updates | Read a session record or update the user's last action. |
| B | 95% reads, 5% updates | View a photo or edit its tags. |
| C | 100% reads | Look up user profiles by key. |
| D | 95% reads, 5% inserts. Reads favor recent records. | Publish status updates and read the newest entries more often. |
| E | 95% short scans, 5% inserts | Read a range of posts in a conversation or add a new post. |
| F | 50% reads, 50% read-modify-write operations | Read a profile or retrieve it to increment a visit counter. |

The [Yanex experiment](experiments.md) starts with profile C. To select a workload in Python, see the [Python guide](python.md).
