#!/bin/bash
# Runs the quick Hive queries and saves the output to docs/hive_quick_results.txt.
cd /home/hadoop/hive_meta
hive --hiveconf hive.cli.print.header=true -f /home/hadoop/vestiq/04_hive/quick_queries.hql | tee /home/hadoop/vestiq/docs/hive_quick_results.txt
