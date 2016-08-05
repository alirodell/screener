#!/usr/bin/python

import requests
import datetime
import boto3
import logging
import os
import sys
import time
import pip

def main():
    installed_packages = pip.get_installed_distributions()
    
    python_version_correct = False
    
    boto3_installed = False
    botocore_installed = False
    requests_installed = False
    
    if sys.version_info.major >= 3: 
        print("You are running on Python 3.")
        python_version_correct = True
    
    for x in installed_packages:
        if(x.project_name == 'boto3'): 
            print("boto3 is installed.")
            boto3_installed = True
        
        if(x.project_name == 'botocore'): 
            print("botocore is installed.")
            botocore_installed = True
        
        if(x.project_name == 'requests'): 
            print("requests is installed.")
            requests_installed = True
            
    if(python_version_correct and boto3_installed and botocore_installed and requests_installed): print("\nBase configs are all installed, you are on the correct version of Python and you have the correct packages installed.")
    
    dynamodb_ok = False
    s3_ok = False
    # Now check the AWS resources.
    try:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://dynamodb.us-east-1.amazonaws.com")
        dynamodb_ok = True
    except: print("Had an issue connecting to the Dynamodb instance.")
    
    try:    
        s3_outputs = boto3.resource('s3')
        rodell_info_bucket = s3_outputs.Bucket('rodell.info')
        output_bucket = s3_outputs.Bucket('rodell-screener-output')
        input_bucket = s3_outputs.Bucket('rodell-screener-input')
        s3_ok = True
    except: print("Had an issue connecting to S3")
    
    if dynamodb_ok and s3_ok: print("\nAWS resources check out OK.")
    

    
    
    
    
    
if __name__ == "__main__": main()