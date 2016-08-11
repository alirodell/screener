#!/usr/bin/python

import boto3
import requests
import datetime
from boto3.dynamodb.conditions import Key, Attr




def main():

    def split_and_make_date(date_string):
        s = date_string.split('-')
        year = int(s[0])
        month = int(s[1])
        day = int(s[2])
        
        return datetime.date(year, month, day)
    
    def get_security_close_price(desired_date, stock_symbol):
        yahoo_query_url = 'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.historicaldata%20where%20symbol%20%3D%20%22###%22%20and%20startDate%20%3D%20%22SSSS%22%20and%20endDate%20%3D%20%22EEEE%22&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback='    
        
        specific_query = yahoo_query_url.replace('SSSS', str(desired_date))
        specific_query = specific_query.replace("EEEE", str(desired_date))
        specific_query = specific_query.replace("###",stock_symbol)
                
        hist_resp = requests.get(specific_query)
        
        bulk_response = hist_resp.json()['query']
        
        results_dict = bulk_response['results']
        
        quote_list = results_dict['quote']
        
        return float(quote_list['Close'])
    
    the_stocks = ["AMD", "HSTM", "GRPN", "EBAY", "MET", "NVDA", "TWTR", "MSFT", "NFLX", "AAPL", "C", "ANTH", "APOL","RCII","TROW","DVAX","BMRN","LLTC","PRGX","ASML","MFRI","TTGT","CELG","VNOM","TITN","ININ","XENE","ILMN"]

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://dynamodb.us-east-1.amazonaws.com")
    #print("Opening the trend history table.")
    trend_history_table = dynamodb.Table('Trend_History') 
    
    # Loop through and select the trend history for each stock in the list.
    # For each stock we parse out the date of each trend and if it has been at least 30 days, we determine the price change of the stock since the trend identification. 
    # Prices for those dates are selected from Yahoo finance.
    
    # Note: We started collecting trends on 11-July-2016.  Using that date as the first trend is not valid so we should discount that one.
    
    for security in the_stocks:
        trend_dict = trend_history_table.query(
            KeyConditionExpression=Key('stock_symbol').eq(security)                               
        )
        
        if trend_dict['Count'] > 0: 
            print("We have {} trend instances for {}.".format(trend_dict['Count'], security))
   
            # Loop through the items which is a list of dictionaries.
            for x in trend_dict['Items']:
                
                trend_date = split_and_make_date(x['occurence_date'])
                
                if trend_date > split_and_make_date('2016-07-11'):
                    
                    print("\t{} has a {} signal on {}".format(x['stock_symbol'], x['trend_type'], x['occurence_date']))
                
                
                    
                    
                    #print(type(trend_date))
                    trend_date_plus_thirty = trend_date + datetime.timedelta(days=30)
                    #print(trend_date)
                    #print(trend_date_plus_thirty)
                    
                    # Don't do analysis for trends that are less than 30 days old.
                    if trend_date_plus_thirty < datetime.date.today(): 
                        trend_date_close = get_security_close_price(trend_date, x['stock_symbol'])
                        thirty_day_close = get_security_close_price(trend_date_plus_thirty, x['stock_symbol'])
                        print("\t\tClose price on {} was {}".format(trend_date, trend_date_close))
                        print("\t\tClose price on {} was {}".format(trend_date_plus_thirty, thirty_day_close))
                        print("\t\tWhich represents a {} increase.".format((thirty_day_close - trend_date_close) / trend_date_close))
                    else:
                        print("\t\tNot enough days have passed to show performance for this trend.")
                        

 
 
 
if __name__ == "__main__": main()