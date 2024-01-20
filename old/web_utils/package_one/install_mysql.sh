#!/usr/bin/bash

sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation

# clcik no, click y four times
# enter sudo mysql
# FLUSH PRIVILEGES;
# ALTER USER 'root'@'localhost' IDENTIFIED BY '0000';
