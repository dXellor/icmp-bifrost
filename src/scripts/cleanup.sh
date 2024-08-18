#!/bin/bash

function catch_error {
    $@ > /dev/null 2>&1
}

if [ $# -ne 2 ]; then
    echo "No arguments provided: CLIENT_IP, SERVER_IP";
    exit -1;
fi

CLIENT_IP=$1
SERVER_IP=$2

ip tuntap delete tun0b mode tun;

catch_error "iptables -t mangle -D INPUT -s $SERVER_IP -p icmp -j NFQUEUE --queue-num 1";
catch_error "iptables -t mangle -D INPUT -s $CLIENT_IP -p icmp -j NFQUEUE --queue-num 1";
catch_error "iptables -t nat -D POSTROUTING -j MASQUERADE";
