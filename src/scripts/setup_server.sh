#!/bin/bash

function exit_if_error {
    $@
    local ec=$?
    if (( $? != 0 )); then
        exit $ec
    fi
}

if [ $# -ne 2 ]; then
    echo "No arguments provided: CLIENT_IP, NET_INTERFACE";
    exit -1;
fi

CLIENT_IP=$1
NET_INTERFACE=$2

exit_if_error "ip tuntap add name tungame mode tun";
exit_if_error "ip link set tun0b up";
exit_if_error "ip addr add 10.0.0.3/24 dev tun0b";

exit_if_error "iptables -t mangle -A INPUT -s $CLIENT_IP -p icmp -j NFQUEUE --queue-num 1";
exit_if_error "iptables -t nat -A POSTROUTING -o $NET_INTERFACE -j MASQUERADE";