#!/bin/bash

echo --- Setting up Prerequisites
export FLASK_APP=dashboard.py

sudo apt-get update
sudo apt-get install mysql-server # Install MySQL
sudo apt-get install python3 # Install Python3
sudo apt-get install python3-pip # Install Pip3

sudo service mysql start

pip3 install -r requirements.txt


# TODO: investigate mysql executions
