#!/bin/bash

if [ $# -eq 0 ]; then
    echo "No client ip address supplied";
    exit -1;
fi

sudo iptables -t mangle -I PREROUTING -s $1 -p icmp -j MARK --set-mark 7132
sudo iptables -t mangle -I INPUT -s $1 -p icmp -j NFQUEUE --queue-num 1

# sudo iptables -t mangle -I PREROUTING -s 0.0.0.0/0 -j MARK --set-mark 7133;
# sudo iptables -t mangle -I INPUT -s 0.0.0.0/0 -j NFQUEUE --queue-num 1;
