#!/bin/bash
# setups load balancer
sudo apt-get update
sudo apt install -y net-tools
sudo apt install -y  haproxy
sudo apt install -y nginx
sudo apt install -y certbot
sudo apt-get -y install software-properties-common
sudo systemctl restart haproxy
