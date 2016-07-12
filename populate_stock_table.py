#!/usr/bin/python

import boto3

def main():
    
    
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
    #dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://dynamodb.us-east-1.amazonaws.com")

    stock_list_table = dynamodb.Table('Stock_List')
    stock_list_table.delete()
    
    # There is one entry per stock symbol in this table.
    stock_list_table = dynamodb.create_table(
        TableName='Stock_List',
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
            'ReadCapacityUnits': 2,
            'WriteCapacityUnits': 2
        }
    )

    print("Stock List Table status:", stock_list_table.table_status)

        
    
    nasdaq_company_list = open('NASDAQ.csv')
    nyse_company_list = open('NYSE.csv')
    amex_company_list = open('AMEX.csv')

    the_stocks = []
    for line in nasdaq_company_list:
        
        # Skip the first line since it's the column headers and filter out any strange symbols that we don't want to look at.
        if(line.find("Symbol") != -1 or line.find("n/a") != -1): pass
        else:
            data_list = line.split(',')
            stock_list_table.put_item( Item = { 'stock_symbol': data_list[0].strip('"') } ) 
           
    print(stock_list_table.scan())
    
    for line in nyse_company_list:
    
        # Skip the first line since it's the column headers and filter out any strange symbols that we don't want to look at.
        if(line.find("Symbol") != -1 or line.find("n/a") != -1): pass
        else:
            data_list = line.split(',')
            stock_list_table.put_item( Item = { 'stock_symbol': data_list[0].strip('"') } )
    
    print(stock_list_table.scan())
    
    for line in amex_company_list:
    
        # Skip the first line since it's the column headers and filter out any strange symbols that we don't want to look at.
        if(line.find("Symbol") != -1 or line.find("n/a") != -1): pass
        else:
            data_list = line.split(',')
            stock_list_table.put_item( Item = { 'stock_symbol': data_list[0].strip('"') } )
    
    print(stock_list_table.scan())
    
if __name__ == "__main__": main()