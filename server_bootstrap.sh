#!/bin/bash

sudo yum -y install python34
sudo alternatives --set python /usr/bin/python3.4
sudo yum -y install python34-pip
sudo yum -y install git
sudo pip install boto3
sudo pip install botocore
sudo pip install requests
git init
git clone https://github.com/alirodell/screener.git

