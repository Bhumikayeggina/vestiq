#!/bin/bash
# Runs the Spark SQL job, then the MLlib job, both on YARN (1 executor with 2 cores: the link between VMs is slow).
OPTS="--master yarn --num-executors 1 --executor-cores 2 --executor-memory 1g --conf spark.executor.memoryOverhead=384m --conf spark.hadoop.dfs.replication=1 --conf spark.sql.shuffle.partitions=8"
spark-submit $OPTS /home/hadoop/vestiq/05_spark/features.py 2> /home/hadoop/features.err | tee /home/hadoop/vestiq/docs/spark_sql_results.txt
spark-submit $OPTS /home/hadoop/vestiq/05_spark/ml_kmeans.py 2> /home/hadoop/ml.err | tee /home/hadoop/vestiq/docs/spark_ml_results.txt
