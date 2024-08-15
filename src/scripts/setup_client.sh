#!/bin/bash

function exit_if_error {
    $@
    local ec=$?
    if (( $? != 0 )); then
        exit $ec
    fi
}

if [ $# -ne 1 ]; then
    echo "No argument provided: SERVER_IP";
    exit -1;
fi

SERVER_IP=$1

exit_if_error "ip tuntap add name tun0b mode tun";
exit_if_error "ip link set tun0b up";
exit_if_error "ip addr add 10.0.0.2 peer 10.0.0.1 dev tun0b";
exit_if_error "ip route add default via 10.0.0.1 dev tun0b";

exit_if_error "iptables -t mangle -A INPUT -s $SERVER_IP -p icmp -j NFQUEUE --queue-num 1";