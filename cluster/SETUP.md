# Cluster setup

1. **VMs:** VirtualBox, Ubuntu Server 22.04, user `hadoop`. Settings used: 2 vCPU, 4 GB RAM, Paravirtualization None,
   PS/2 mouse, VBoxSVGA without 3D, audio and USB off. Adapter 1 NAT (SSH port forward), Adapter 2 Bridged (cluster network).
2. **Network:** `enp0s8` on DHCP, names in `/etc/hosts` (`master`, `worker2`, `worker3`).
   After a network change run `cluster/fix_hosts.sh MASTER_IP WORKER2_IP WORKER3_IP`.
3. **SSH:** key pair on the master, copied to all three nodes with `ssh-copy-id`.
4. **Software:** OpenJDK 8; Hadoop 3.3.6, Spark 3.5.3, Hive 3.1.3 and Pig 0.17.0 unpacked in the home folder.
   Spark is installed on all nodes and uses `local:` jars. Hive and Pig are only needed on the master.
5. **Configuration:** `cluster/conf` holds core-site, hdfs-site, yarn-site, mapred-site, workers and spark-defaults.
   Replication is 2. YARN allows 2048 MB and 2 vCores per node.
6. **First start:** `hdfs namenode -format` once, then `cluster/start_cluster.sh`. Stop with `cluster/stop_cluster.sh`.
7. **Check:** `cluster/checkpoint.sh` prints OK or MISSING for every component.
8. **Hive:** `schematool -dbType derby -initSchema` once, and always run Hive from `~/hive_meta`.
