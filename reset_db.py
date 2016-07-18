from __future__ import print_function # Python 2/3 compatibility
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
#dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://dynamodb.us-east-1.amazonaws.com")
#
# Interesting thing to note is that when you create the tables you only define the keys.  Not the other attributes.
#

current_trend_table = dynamodb.Table('Current_Trend')
current_trend_table.delete()


trend_history_table = dynamodb.Table('Trend_History')
trend_history_table.delete()

print("Tables Deleted.")



# There is one entry per stock symbol in this table.
new_current_trend_table = dynamodb.create_table(
    TableName='Current_Trend',
    KeySchema=[
        {
            'AttributeName': 'stock_symbol',
            'KeyType': 'HASH'  #Partition key
        },
    ],
    AttributeDefinitions=[
        {         
            'AttributeName': 'stock_symbol',
            'AttributeType': 'S'
        }

    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 50,
        'WriteCapacityUnits': 50
    }
)

print("Current Trend Table status:", new_current_trend_table.table_status)

# There will be many entries per stock symbol in this table.
new_trend_history_table = dynamodb.create_table(
    TableName='Trend_History',
    KeySchema=[
        {
            'AttributeName': 'stock_symbol',
            'KeyType': 'HASH'  #Partition key
        },
        {
            'AttributeName': 'occurence_date',
            'KeyType': 'RANGE'  #Partition key
        },        
    ],
    AttributeDefinitions=[
        {         
            'AttributeName': 'stock_symbol',
            'AttributeType': 'S'
        },   
        {
            'AttributeName': 'occurence_date',
            'AttributeType': 'S'
        },
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 50,
        'WriteCapacityUnits': 50
    }
)

print("Trend History Table status:", new_trend_history_table.table_status)

