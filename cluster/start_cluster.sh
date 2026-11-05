#!/bin/bash
# Starts HDFS, YARN and the MapReduce history server, then shows what is running.
start-dfs.sh
start-yarn.sh
mapred --daemon start historyserver
sleep 5
jps
hdfs dfsadmin -report | head -12
