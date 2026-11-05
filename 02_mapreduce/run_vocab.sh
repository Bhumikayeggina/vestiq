#!/bin/bash
# Runs the vocabulary job with Hadoop Streaming on YARN.
# The combiner sums counts inside each mapper first, so very little data crosses the slow network.
hdfs dfs -rm -r -f /vestiq/staging/vocab
hadoop jar /home/hadoop/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
  -D mapreduce.job.reduces=1 -D dfs.replication=1 \
  -files /home/hadoop/vestiq/02_mapreduce/mapper.py,/home/hadoop/vestiq/02_mapreduce/reducer.py \
  -mapper "python3 mapper.py" -combiner "python3 reducer.py" -reducer "python3 reducer.py" \
  -input /vestiq/curated/myntra_clean -output /vestiq/staging/vocab
