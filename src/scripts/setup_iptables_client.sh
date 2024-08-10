#!/bin/bash

if [ $# -ne 2 ]; then
    echo "No arguments provided: client_ip, server_ip";
    exit -1;
fi

MARK_TO_SERVER=7130
MARK_FROM_SERVER=7131
CLIENT_IP=$1
SERVER_IP=$2

sudo iptables -t mangle -I OUTPUT -s $CLIENT_IP ! -p icmp -j MARK --set-mark $MARK_TO_SERVER;
sudo iptables -t mangle -I POSTROUTING -s $CLIENT_IP -j NFQUEUE --queue-num 1;

sudo iptables -t mangle -I PREROUTING -s $SERVER_IP -p icmp -j MARK --set-mark $MARK_FROM_SERVER;
sudo iptables -t mangle -I INPUT -s $SERVER_IP -p icmp -j NFQUEUE --queue-num 1;
