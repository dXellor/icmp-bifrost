#!/bin/bash

function catch_error {
    $@ > /dev/null 2>&1
}

if [ $# -ne 3 ]; then
    echo "No arguments provided: CLIENT_IP, SERVER_IP, NET_INTERFACE";
    exit -1;
fi

CLIENT_IP=$1
SERVER_IP=$2
NET_INTERFACE=$3

ip tuntap delete tun0b mode tun;

catch_error "iptables -D FORWARD -s 10.0.0.0/24 -j ACCEPT"
catch_error "iptables -D FORWARD -d 10.0.0.0/24 -j ACCEPT"
catch_error "iptables -t mangle -D INPUT -s $SERVER_IP -p icmp -j NFQUEUE --queue-num 1";
catch_error "iptables -t mangle -D INPUT -s $CLIENT_IP -p icmp -j NFQUEUE --queue-num 1";
catch_error "iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o $NET_INTERFACE -j MASQUERADE";
