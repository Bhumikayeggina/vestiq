#!/bin/bash
# Runs the cleaning job on YARN with 1 executor (the multi-line CSV can only be read by one task).
# Output replication is 1 so the cleaned data does not cross the slow network.
spark-submit --master yarn \
  --num-executors 1 --executor-memory 1g \
  --conf spark.executor.memoryOverhead=384m \
  --conf spark.hadoop.dfs.replication=1 \
  ~/vestiq/05_spark/clean_myntra.py
