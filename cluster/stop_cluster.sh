#!/bin/bash
# Stops everything cleanly (always do this before saving or shutting down the VMs).
mapred --daemon stop historyserver
stop-yarn.sh
stop-dfs.sh
