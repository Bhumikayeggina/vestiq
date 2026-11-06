#!/bin/bash
# Usage: fix_hosts.sh MASTER_IP WORKER2_IP WORKER3_IP
# Rewrites the master/worker2/worker3 lines in /etc/hosts on all three VMs after a network change.
M=$1; W2=$2; W3=$3
if [ -z "$W3" ]; then echo "Usage: $0 MASTER_IP WORKER2_IP WORKER3_IP"; exit 1; fi

# the master itself
sudo sed -i '/ master$/d;/ worker2$/d;/ worker3$/d' /etc/hosts
printf '%s master\n%s worker2\n%s worker3\n' "$M" "$W2" "$W3" | sudo tee -a /etc/hosts > /dev/null

# the two workers, reached by their new addresses (each asks for the hadoop password once)
for IP in "$W2" "$W3"; do
  ssh -t -o StrictHostKeyChecking=no hadoop@"$IP" "sudo sed -i '/ master\$/d;/ worker2\$/d;/ worker3\$/d' /etc/hosts && printf '%s master\n%s worker2\n%s worker3\n' '$M' '$W2' '$W3' | sudo tee -a /etc/hosts > /dev/null"
done
echo "Done. Check with: cat /etc/hosts"
