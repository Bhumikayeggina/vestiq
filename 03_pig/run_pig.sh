#!/bin/bash
# Runs the Pig analytics script as MapReduce jobs on YARN (old outputs are removed first).
hdfs dfs -rm -r -f /vestiq/staging/pig_brand_stats /vestiq/staging/pig_category_stats
pig -x mapreduce /home/hadoop/vestiq/03_pig/brand_stats.pig
