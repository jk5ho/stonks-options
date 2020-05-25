#!/bin/bash

echo --- Setting up Prerequisites
export FLASK_APP=dashboard.py

apt-get update
apt-get install mysql-server # Install MySQL
apt-get install python3 # Install Python3
apt-get install python3-pip # Install Pip3

pip3 install -r requirements.txt


# TODO: investigate mysql executions
