#!/bin/bash 

placa_lan=vmnet1
placa_wan=wlp2s0

#modprobe iptable_nat
#echo 1 > /proc/sys/net/ipv4/ip_forward

#sysctl net.ipv4.ip_forward=1

#iptables -F
iptables -t nat -A POSTROUTING -o $placa_wan -j MASQUERADE
iptables -A FORWARD -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i $placa_lan -o $placa_wan -j ACCEPT
