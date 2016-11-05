#!/bin/bash

sudo yum -y install python34
sudo alternatives --set python /usr/bin/python3.4
sudo yum -y install python34-pip
sudo yum -y install git
sudo yum -y install dos2unix
sudo pip install boto3
sudo pip install botocore
sudo pip install requests
cd /home/ec2-user
git init
git clone https://github.com/alirodell/screener.git
sudo chown -R ec2-user:ec2-user /home/ec2-user/screener/
chmod +x /home/ec2-user/screener/test_env.py
/home/ec2-user/screener/test_env.py > /home/ec2-user/screener/test_output.txt
