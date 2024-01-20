#!/usr/bin/bash

#sudo systemctl stop mysql
sudo apt purge mysql-server
sudo apt purge mysql-server mysql-client mysql-common mysql-server-core-* mysql-client-core-*
dpkg -l | grep mysql
sudo rm -rf /var/lib/mysql
sudo rm /etc/apt/sources.list.d/mysql.list
sudo apt update
