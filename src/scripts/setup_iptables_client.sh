#!/bin/bash

if [ $# -eq 0 ]; then    
    echo "No server ip address supplied";
    exit -1;
fi

sudo iptables -t mangle -I PREROUTING -s 0.0.0.0/0 -j MARK --set-mark 7130;
sudo iptables -t mangle -I INPUT -s 0.0.0.0/0 -j NFQUEUE --queue-num 1;

# sudo iptables -t mangle -I PREROUTING -s $1 -p icmp -j MARK --set-mark 7131
# sudo iptables -t mangle -I INPUT -s $1 -p icmp -j NFQUEUE --queue-num 1