# Changelog

## Unreleased

- Group code, experiments, runners, and documentation by benchmark. Keep the existing YCSB imports.
- Use read-only profile C for the default experiment. Pin the default YCSB image to 0.1.0.

- Install BONDI 0.4 from PyPI for MongoDB and Couchbase benchmarks.

- Port the YCSB runner for MongoDB and Couchbase, including workload configuration, validated phase results and a disposable Yanex experiment.
- Publish versioned multi-platform YCSB images to GHCR and pull missing runner images automatically.
