#!/bin/sh
set -eu
binding=$1
phase=$2
profile=$3
case "$binding" in
    mongodb) client=site.ycsb.db.MongoDbClient ;;
    couchbase2) client=site.ycsb.db.couchbase2.Couchbase2Client ;;
    *) exit 2 ;;
esac
case "$phase" in load) mode=-load ;; run) mode=-t ;; *) exit 2 ;; esac
cd "/opt/ycsb/$binding"
exec java -cp 'conf:lib/*' site.ycsb.Client "$mode" -db "$client" -P "workloads/workload$profile" -P /dev/stdin
