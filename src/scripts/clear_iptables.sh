#!/bin/bash

if [ $# -ne 2 ]; then
    echo "No arguments provided: client_ip, server_ip";
    exit -1;
fi

MARK_TO_SERVER=7130
MARK_FROM_SERVER=7131
MARK_FROM_CLIENT=7132
MARK_TO_CLIENT=7133
CLIENT_IP=$1
SERVER_IP=$2

# Client rules
sudo iptables -t mangle -D OUTPUT -s $CLIENT_IP ! -p icmp -j MARK --set-mark $MARK_TO_SERVER > /dev/null 2>&1;
sudo iptables -t mangle -D POSTROUTING -s $CLIENT_IP -j NFQUEUE --queue-num 1 > /dev/null 2>&1;

sudo iptables -t mangle -D PREROUTING -s $SERVER_IP -p icmp -j MARK --set-mark $MARK_FROM_SERVER > /dev/null 2>&1;
sudo iptables -t mangle -D INPUT -s $SERVER_IP -p icmp -j NFQUEUE --queue-num 1 > /dev/null 2>&1;

# Server rules
sudo iptables -t mangle -D PREROUTING -s $CLIENT_IP -p icmp -j MARK --set-mark $MARK_FROM_CLIENT > /dev/null 2>&1;
sudo iptables -t mangle -D INPUT -s $CLIENT_IP -p icmp -j NFQUEUE --queue-num 1 > /dev/null 2>&1;

sudo iptables -t mangle -D PREROUTING ! -s $CLIENT_IP -d $SERVER_IP -p tcp -j MARK --set-mark $MARK_TO_CLIENT > /dev/null 2>&1;
sudo iptables -t mangle -D INPUT ! -s $CLIENT_IP -d $SERVER_IP -j NFQUEUE --queue-num 1 > /dev/null 2>&1;
