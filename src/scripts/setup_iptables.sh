#!/bin/bash

sudo iptables -t mangle -I PREROUTING -s 0.0.0.0/0 -j MARK --set-mark 7130
sudo iptables -t mangle -I INPUT -s 0.0.0.0/0 -j NFQUEUE --queue-num 1

sudo iptables -t mangle -I PREROUTING -s server_ip -p icmp -j MARK --set-mark 7131
sudo iptables -t mangle -I INPUT -s server_ip -p icmp -j NFQUEUE --queue-num 1