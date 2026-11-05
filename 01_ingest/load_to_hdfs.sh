#!/bin/bash
# Vestiq stage 1: load the raw Myntra dataset into HDFS (done once on the cluster).
# Dataset: Myntra Products Dataset (Kaggle, Ronak Bokaria, CC0), 1,060,213 products, about 1.3 GB.
# Do NOT re-run the put during a demo (slow network). Use check_hdfs.sh instead.
hdfs dfs -mkdir -p /user/hadoop
hdfs dfs -mkdir -p /vestiq/raw /vestiq/staging /vestiq/curated /vestiq/output
hdfs dfs -put /home/hadoop/myntra202305041052.csv /vestiq/raw/
