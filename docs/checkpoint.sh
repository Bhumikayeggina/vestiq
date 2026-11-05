#!/bin/bash
# Vestiq checkpoint: prints OK or MISSING for each part of the project. Changes nothing.
chk() { desc="$1"; shift; if "$@" >/dev/null 2>&1; then echo "[ OK ]    $desc"; else echo "[MISSING] $desc"; fi; }

echo "=== A/B. Machines and Hadoop services ==="
chk "passwordless ssh to worker2" ssh -o BatchMode=yes -o ConnectTimeout=5 worker2 true
chk "passwordless ssh to worker3" ssh -o BatchMode=yes -o ConnectTimeout=5 worker3 true
chk "NameNode running" bash -c "jps | grep -q NameNode"
chk "ResourceManager running" bash -c "jps | grep -q ResourceManager"
chk "2 live DataNodes" bash -c "hdfs dfsadmin -report | grep -q 'Live datanodes (2)'"

echo "=== C. Data in HDFS ==="
chk "raw Myntra file in HDFS" hdfs dfs -test -e /vestiq/raw/myntra202305041052.csv
chk "HDFS folders created" hdfs dfs -test -d /vestiq/curated

echo "=== D. Tools ==="
chk "Spark on master" test -x /home/hadoop/spark/bin/spark-submit
chk "Spark on worker2" ssh worker2 test -x /home/hadoop/spark/bin/spark-submit
chk "Spark on worker3" ssh worker3 test -x /home/hadoop/spark/bin/spark-submit
chk "Spark settings file" test -s /home/hadoop/spark/conf/spark-defaults.conf
chk "Hive installed" test -x /home/hadoop/hive/bin/hive
chk "Hive database initialised" test -d /home/hadoop/hive_meta/metastore_db
chk "Pig installed" test -x /home/hadoop/pig/bin/pig

echo "=== F. Code files ==="
for f in 05_spark/clean_myntra.py 05_spark/run_clean.sh 02_mapreduce/mapper.py 02_mapreduce/reducer.py 02_mapreduce/run_vocab.sh cluster/conf/core-site.xml .gitignore; do
  chk "$f" test -s /home/hadoop/vestiq/$f
done

echo "=== G. Job outputs ==="
chk "cleaned data (Spark job finished)" hdfs dfs -test -e /vestiq/curated/myntra_clean/_SUCCESS
chk "vocabulary (MapReduce job finished)" hdfs dfs -test -e /vestiq/staging/vocab/_SUCCESS

echo "=== E. GitHub ==="
chk "everything committed and pushed" bash -c 'cd /home/hadoop/vestiq && [ -z "$(git status --porcelain)" ] && [ "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)" ]'
