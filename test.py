from __future__ import print_function # Python 2/3 compatibility
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")


table = dynamodb.Table('Current_Trend')

table.put_item(
        Item={
              'stock_symbol': 'AMD',
              'up-trend': False,
              'down-trend': True,
              'trend_start_date': '2016-07-06'   
        }
    )

response = table.get_item(
    Key={
        'stock_symbol': 'AMD'
    }
)

print(response)
print("All Done.")


