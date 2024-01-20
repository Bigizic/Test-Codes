#!/bin/bash
# bash script for new server, proceeds to install certain libraries and packages
sudo apt-get update
sudo apt-get install python3-lxml -y
sudo apt install gunicorn -y
sudo apt-get install libmariadbclient-dev -y
sudo apt-get install libmysqlclient-dev -y
sudo apt install python3-pip -y
sudo apt-get install -y libffi-dev
sudo apt-get install -y libssl-dev
sudo apt-get install -y build-essential
sudo apt-get install -y python3.4-dev
sudo apt-get install -y libpython3-dev
sudo apt install mysql-server -y
sudo apt-get update
sudo apt-get upgrade
