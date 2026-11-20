# YCSB prototype

The first implementation runs YCSB in a pinned Docker image against MongoDB and Couchbase.
The Yanex example provisions a disposable database and records separate load and run results.

---

## Interpreting updates

With the pinned Couchbase KV binding, a single-field update replaces the entire document.
Use the SQL++ path for partial updates, or configure full-record updates on both systems.
See the [workload options](../ycsb.md).
