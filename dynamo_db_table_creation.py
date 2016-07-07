from __future__ import print_function # Python 2/3 compatibility
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

#
# Interesting thing to note is that when you create the tables you only define the keys.  Not the other attributes.
#


# There is one entry per stock symbol in this table.
current_trend_table = dynamodb.create_table(
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
        'ReadCapacityUnits': 1,
        'WriteCapacityUnits': 1
    }
)

print("Current Trend Table status:", current_trend_table.table_status)

# There will be many entries per stock symbol in this table.
trend_history_table = dynamodb.create_table(
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
        'ReadCapacityUnits': 1,
        'WriteCapacityUnits': 1
    }
)

print("Trend History Table status:", trend_history_table.table_status)

