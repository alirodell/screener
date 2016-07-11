from __future__ import print_function # Python 2/3 compatibility
import boto3

#dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

print("Attempting to connect to the db in AWS.")
dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://dynamodb.us-east-1.amazonaws.com")
                    
                    
#current_trend_table = dynamodb.Table('Current_Trend')
print("Opening the current trend table.")    
table = dynamodb.Table('Current_Trend')

print("Opening the trend history table.")
trend_history_table = dynamodb.Table('Trend_History') 
#table.put_item(
#        Item={
#              'stock_symbol': 'AMD',
#              'up-trend': False,
#              'down-trend': True,
#              'trend_start_date': '2016-07-06'   
#        }
#    )

#response = table.get_item(
#    Key={
#        'stock_symbol': 'AMD'
#    }
#)

print("Scanning the tables.")

scan_table = table.scan()
history = trend_history_table.scan()
print(scan_table)

print(history)


#print(response)
print("All Done.")


