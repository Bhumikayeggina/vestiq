#!/bin/bash
# Shows that the data is in HDFS, replicated across both DataNodes (safe to run any time).
hdfs dfsadmin -report | head -12
hdfs dfs -ls -h /vestiq/raw
hdfs fsck /vestiq/raw -files -blocks -locations | tail -15
