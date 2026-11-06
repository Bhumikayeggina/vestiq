# Demo script

## 30 minutes before
1. Plug in all three laptops, same Wi-Fi, sleep off. Start the three VMs (Headless Start) and wait about 10 minutes.
2. In each VM: `ip -4 -br addr show enp0s8`. On the master:
   `~/vestiq/cluster/fix_hosts.sh MASTER_IP WORKER2_IP WORKER3_IP`
3. `~/vestiq/cluster/start_cluster.sh`
4. `~/vestiq/cluster/checkpoint.sh` must show all OK.
5. Browser tabs: HDFS (port 9870), YARN (8088), history server (19888), the app (https://vestiq.streamlit.app).

## Flow (about 8 minutes)
1. **Architecture:** the diagram in the README.
2. **Cluster:** YARN Nodes page (2 nodes), HDFS Datanodes page (2 live).
3. **Data in HDFS:** `~/vestiq/01_ingest/check_hdfs.sh` (1.3 GB, replication 2).
4. **Spark on YARN, live:** `spark-submit $SPARK_HOME/examples/src/main/python/pi.py 20`. Show the application RUNNING in YARN and the Spark UI on port 4040.
   Then show the real job with `nano -v ~/vestiq/05_spark/clean_myntra.py`.
5. **MapReduce:** show `mapper.py` and `reducer.py`, then
   `hdfs dfs -cat /vestiq/staging/vocab/part-* | sort -t$'\t' -k2 -nr | head`.
6. **Pig:** show `03_pig/brand_stats.pig` and `hdfs dfs -cat /vestiq/staging/pig_brand_stats/part-* | head`.
7. **Hive:** `~/vestiq/04_hive/run_quick.sh`.
8. **Spark SQL and MLlib:** `cat ~/vestiq/docs/spark_sql_results.txt` and `cat ~/vestiq/docs/results/segments.txt`.
9. **App:** search "simple traditional kurti for wedding under 1500".

## Do not run live
`run_clean.sh` (5 to 25 min), `run_all.sh`, large Hive aggregations, any big `hdfs put`, and never `hdfs namenode -format`.

## Likely questions
- **Why replication 2?** There are two DataNodes, so each block exists on both.
- **Why replication 1 for derived data?** The link between the VMs was only 60 to 200 kB/s, and raw data stays safe at 2.
- **Why one executor for cleaning?** A CSV with line breaks inside quoted fields cannot be split, so one task reads it.
- **Why are most Hive queries in Spark SQL?** Hive on MapReduce submits a job per query, too slow on this network.
- **What is the Bayesian rating?** It pulls ratings with few votes towards the global mean, so one 5-star vote doesn't beat 5,000 votes at 4.5.
- **Limitations?** May 2023 snapshot, no purchase history (no personalisation), hand-made synonym list.
