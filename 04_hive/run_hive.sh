#!/bin/bash
# Creates the Hive table, then runs the 10 queries and saves the results to docs/hive_results.txt.
# Hive must be started from ~/hive_meta, where its local database lives.
cd /home/hadoop/hive_meta
hive -f /home/hadoop/vestiq/04_hive/create_tables.hql
hive --hiveconf hive.cli.print.header=true -f /home/hadoop/vestiq/04_hive/queries.hql | tee /home/hadoop/vestiq/docs/hive_results.txt
