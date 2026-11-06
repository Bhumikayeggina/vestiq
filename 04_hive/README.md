# Hive stage

- `create_tables.hql`: external table `vestiq.products` over the cleaned data in HDFS.
- `quick_queries.hql` and `run_quick.sh`: schema and filter queries that Hive answers without launching a job (used in the demo).
- `queries.hql` and `run_hive.sh`: the full set of 10 aggregate queries. On Hive-on-MapReduce every query is a separate
  YARN job, which took far too long on this cluster's slow inter-node network, so the same analytics were run in Spark SQL
  (`05_spark/features.py`, results in `docs/spark_sql_results.txt`). The full set is kept for reference.
