#!/bin/bash

if [ $# -ne 2 ]; then
    echo "No arguments provided: client_ip, server_ip";
    exit -1;
fi

MARK_FROM_CLIENT=7132
MARK_TO_CLIENT=7133
CLIENT_IP=$1
SERVER_IP=$2

sudo iptables -t mangle -I PREROUTING -s $CLIENT_IP -p icmp -j MARK --set-mark $MARK_FROM_CLIENT;
sudo iptables -t mangle -I INPUT -s $CLIENT_IP -p icmp -j NFQUEUE --queue-num 1;

sudo iptables -t mangle -I PREROUTING ! -s $CLIENT_IP -d $SERVER_IP -j MARK --set-mark $MARK_TO_CLIENT;
sudo iptables -t mangle -I INPUT ! -s $CLIENT_IP -d $SERVER_IP -j NFQUEUE --queue-num 1;
