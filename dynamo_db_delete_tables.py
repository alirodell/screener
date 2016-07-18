from __future__ import print_function # Python 2/3 compatibility
import boto3

#dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://dynamodb.us-east-1.amazonaws.com")
dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")


# There is one entry per stock symbol in this table.

current_trend_table = dynamodb.Table('Current_Trend')
current_trend_table.delete()


trend_history_table = dynamodb.Table('Trend_History')
trend_history_table.delete()

print("All done.")