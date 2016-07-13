#!/usr/bin/python

import requests
import datetime
import boto3
import logging
from _ctypes import ArgumentError




    # This script queries from Yahoo Finance using their YQL protocol.
    #
    # The YQL request returns a dictionary object of one entry 'query'.
    # This query is also a dictionary object with five list objects in it:
    #    diagnostics
    #    results
    #    lang
    #    created
    #    count
    #
    # We are interested in the results dictionary which then has a 'quotes'
    # key where the value is a list of dictionaries corresponding to each trading day. 
    # This is what we are passing into the "Security" object in the init method.
    ##################################################
    
    # Where we are:
    #  - We are inserting the stock symbol into the YQL statement and then executing it and parsing out results.
    #  - We've got the Security object mostly set up, still need to set up the "set methods"
    #  - The "TradingDay" object is set up and working well, all get/set methods are written and we can sort a list of them.
    #  - We're calculating the 10 day SMA for a security as of the last trading day we have. See Questions on this one.
    #
    ###################################################    
    
     

class TradingDay:
    def __init__(self, sec_trading_data = None):    
        self._data = sec_trading_data      
        self._symbol = ''
        self._open = 0.0
        self._close = 0.0
        self._volume = 0
        self._adj_close = 0.0
        self._low = 0.0
        self._high = 0.0
        self._date = None
 
        try:
            # Assign the day's data to object properties.
            if self._data != None:
                self._symbol = self._data['Symbol']
                self._open = float(self._data['Open'])
                self._close = float(self._data['Close'])
                self._volume = int(self._data['Volume'])
                self._adj_close = float(self._data['Adj_Close'])
                self._low = float(self._data['Low'])
                self._high = float(self._data['High'])
                date_parts = self._data['Date'].split('-')
                self._date = datetime.date(int(date_parts[0]),int(date_parts[1]),int(date_parts[2]))
            else: raise ArgumentError
        except KeyError: logging.info("Threw a key error while populating this trading day.")
        except ArgumentError: logging.info("There is an issue with the arguments passed into the TradingDay class")
    
    # Set this so that you can just call .sort() on a list of these objects and sort them by date.
    def __lt__(self,other):           
        return self.get_date() < other.get_date()
        
    def get_symbol(self):
        return self._symbol
        
    def get_open(self):
        return self._open
        
    def get_close(self):
        return self._close
        
    def get_volume(self):
        return self._volume
        
    def get_adj_close(self):
        return self._adj_close
        
    def get_low(self):
        return self._low
        
    def get_high(self):
        return self._high
        
    def get_date(self):
        return self._date
    
        


class Security:
    def __init__(self, security_data_list = None):
        
        # security_data_list is a list of dictionary objects containing historical prices for the security.
        self._data = security_data_list      
        self._10_day_sma = 0.0
        self._20_day_ema = 0.0
        self._30_day_ema = 0.0
        self._current_day_volume = 0
        self._current_day_close = 0.0
        
        
        # make sure that the list was passed in and that it has 30 days of security prices.
        # Right now we are selecting 124 days of historical data, need to change the date parsing in the query generation process.
        # Still need to add the 30 day compare and build out assigning variables.  Moving out to parsing out the Yahoo query first so we can loop back in.
                
        self._trading_day_list = []
        
        # Each iteration of i will be a dictionary object holding a days trading data which will be passed in with the init function of the TradingDay object.
        if self._data != None:
            for i in self._data:
                #print(i)
                day = TradingDay(i)
               
                self._trading_day_list.append(day)
                
        # This sorts the trading days by date.        
        self._trading_day_list.sort()
        
        num_trd = len(self._trading_day_list)
        
        logging.info("This is the total number of trading days - {}".format(num_trd))
        #print("This is the total number of trading days - {}".format(num_trd))    
               
        # Calculate and assign the moving averages
        self._10_day_sma = self.calc_simple_moving_average(10, num_trd)
        self._20_day_ema = self.calc_exp_moving_average(20, num_trd)
        self._30_day_ema = self.calc_exp_moving_average(30, num_trd)
        
        # Assign the other values - these are all for the current trading day only.
        # We are running this script after the market closes. 
        self._current_day_close = self._trading_day_list[num_trd - 1].get_close()
        self._current_day_volume = self._trading_day_list[num_trd - 1].get_volume()
            
        #print("This is the SMA10 value {}".format(self.get_10_day_sma()))    
            #print("Stock symbol {} and date {}".format(trading_day.get_symbol(), trading_day.get_date()))
    
    def calc_exp_moving_average(self, period = 0, num_trd_days = 0):
                
        ema = 0.0
        
        if period > 0 and num_trd_days > 0:
            # need to calculate the previous days EMA in order to return the EMA.  Need to think on how to do this.
            # -> use the 20 day SMA for that value and do this outside the function.
            # EMA Formula is (Close - EMA(previous day)) * multiplier + EMA(previous day)
            # If there is no EMA from before then you use the SMA.
            
            def calc_ema(close = 0.0, previous_day_ema = 0.0):
                multiplier = 2 / (period + 1)
                return (close - previous_day_ema) * multiplier + previous_day_ema
                        
            
            # First, calculate the SMA from the first available period based on the argument "period"
            initial_sma = self.calc_earliest_simple_moving_average(period,num_trd_days)
            #print("The initial_sma for your stock is {}.".format(initial_sma))
                                  
            
            # Need to define a dictionary of ema's mapping date to EMA value.
            ema_list = {}
            ema = 0.0
            
            # Add the dictionary entries.
            for k in range(period, num_trd_days):
                # First time through just use the initial_sma, otherwise use the previous period ema
                previous_ema = 0.0
                #print("k is {}, the period is {}, and the number_trd_Days is {}".format(k,period,num_trd_days))
                
                if k == period:
                    previous_ema = initial_sma
                else:
                    #print("Yesterdays close was {} and yesterdays ema was {}".format(self._trading_day_list[k-1].get_adj_close(),ema_list[str(self._trading_day_list[k-1].get_date())]))
                    previous_ema = ema_list[str(self._trading_day_list[k-1].get_date())]
                
                #print("The previous day's ema is {}".format(previous_ema))
                #print("The date I'm adding to the dict is {} and the {} day ema for that date is {}".format(str(self._trading_day_list[k].get_date()), period, calc_ema(self._trading_day_list[k].get_adj_close(),previous_ema)))
                #print("--------------------------------")
                ema_list[str(self._trading_day_list[k].get_date())] = calc_ema(self._trading_day_list[k].get_close(),previous_ema)
                
                # Store the last date to return the final EMA.
                if k == num_trd_days-1: ema = calc_ema(self._trading_day_list[k].get_close(),previous_ema)
                
                
            

            #print(last_day)
            #ema = ema_list[last_day]
            
        return ema
    
    # This method will earliest period SMA for a given period based on the trading_day_list
    # that was set in the init function. It returns a float
    # if the value returned is a zero then something went wrong.
    def calc_earliest_simple_moving_average(self, period = 0, num_trd_days = 0):
        sma_10_total = 0.0
        sma = 0.0
        if period > 0 and num_trd_days > 0:
            
            for i in range(period):
                sma_10_total += self._trading_day_list[i].get_close()
                #print("initial sma total is {}".format(sma_10_total))
                sma = sma_10_total / period
        return sma    
     
    # This method will calculate the current SMA for a given period based on the trading_day_list
    # that was set in the init function. It returns a float
    # if the value returned is a zero then something went wrong.
    
    # Checked this against Fidelity reported SMA and they agree.
    def calc_simple_moving_average(self, period = 0, num_trd_days = 0):
        sma_10_total = 0.0
        sma = 0.0
        if period > 0 and num_trd_days > 0:
            
            for i in range(period):
                
                #print("i is {} and the adjusted closing price on {} is {}".format(i, self._trading_day_list[num_trd_days-(i+1)].get_date(), self._trading_day_list[num_trd_days-(i+1)].get_adj_close()))
                
                # Have to add 1 to i since ranges in Python are non-inclusive.
                sma_10_total += self._trading_day_list[num_trd_days-(i+1)].get_close()
                #print("sma total is {}".format(sma_10_total))
                sma = sma_10_total / period
        return sma
    
    def get_10_day_sma(self):
        return self._10_day_sma
    
    def get_20_day_ema(self):
        return self._20_day_ema
    
    def get_30_day_ema(self):
        return self._30_day_ema
    
    def get_raw_data(self):
        return self._data
    
    def get_volume(self):
        return self._current_day_volume
    
    def get_close(self):
        return self._current_day_close


        

def main():
    
    # Set the logging level.
    
    
    

 
    # this is the base URL that will be used to query Yahoo finance for historical pricing data.
    # we will replace the #### string with the stock symbol when looking through the_stocks tuple.
    
    # For the purposes of development I am having the end_date be yesterday so that I can run this during the day.  Usually this will run at night so we can get the close prices.
    end_date = datetime.date.today() - datetime.timedelta(hours=48)
    # Start date is represented by @@@@ in the url.
    # Go back 100 calendar days which should give us around 70 trading days.
    start_date = end_date - datetime.timedelta(days=300)
    today_date_string = str(end_date) 
    
    log_file_name = ".".join(("_".join(("screener", today_date_string)),"log"))
    
    logging.basicConfig(filename=log_file_name,level=logging.INFO)
    
    logging.info("Starting processing for the {} trading day at {}.".format(end_date, datetime.datetime.today()))
    
    historical_data_url = 'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.historicaldata%20where%20symbol%20%3D%20%22###%22%20and%20startDate%20%3D%20%22SSSS%22%20and%20endDate%20%3D%20%22EEEE%22&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback='    
    
    historical_data_url = historical_data_url.replace('SSSS', str(start_date))
    historical_data_url = historical_data_url.replace("EEEE", str(end_date))

    notification_dict = {}

    def tally_notification(symbol = '', trend_type = ''):
        notification_dict[symbol] = trend_type
    
    def save_up_trend(symbol = '', new = False):
        return_code = 0
        
        if(len(symbol) > 0):
            current_trend_table.put_item(
                Item={
                      'stock_symbol': symbol,
                      'up_trend': True,
                      'down_trend': False,
                      'trend_start_date': today_date_string 
                }
            )
            
            # If the trend is new, we also update the trend_history table with an entry of trend. Occurrence 
            if new: 
                trend_history_table.put_item(
                    Item={
                          'stock_symbol': symbol,
                          'occurence_date': today_date_string,
                          'trend_type': 'up'
                    }
                )                
            
            
            return_code = 1
        return return_code 
 
    def save_down_trend(symbol = '', new = False):
        return_code = 0
        
        if(len(symbol) > 0):
            current_trend_table.put_item(
                Item={
                      'stock_symbol': symbol,
                      'up_trend': False,
                      'down_trend': True,
                      'trend_start_date': today_date_string 
                }
            )
            
            if new: 
                trend_history_table.put_item(
                    Item={
                          'stock_symbol': symbol,
                          'occurence_date': today_date_string,
                          'trend_type': 'down'
                    }
                ) 
            
            return_code = 1
        return return_code 
    
        
    
    # This list of stocks we will iterate through to select historical data from yahoo finance.
    # This list -MUST- have at least two stocks in it in order for this script to work.
    #the_stocks = ("AMD", "HSTM")
    
    company_list = open('companylist.csv')

    the_stocks = []
    for line in company_list:
        
        # Skip the first line since it's the column headers and filter out any strange symbols that we don't want to look at.
        if(line.find("Symbol") != -1 or line.find("n/a") != -1): pass
        else:
            stock_symbol_list = line.split(',')
            the_stocks.append(stock_symbol_list[0].strip('"')) 
    
    for k in the_stocks:
        
        logging.info("-----------------Starting work on stock symbol {} at {}.------------------------".format(k, datetime.datetime.today()))
        # Generate the YQL string.
        specific_query = historical_data_url.replace("###",k)
        
        #print(specific_query)
        # I could embed the following in a long one line assignment but I'll never remember what I did later so I'm breaking them out.       
        
        # Generally speaking, I am going to log errors and then move on.  Yahoo will likely act a bit differently over time with new stocks, etc.
        try:        
            hist_resp = requests.get(specific_query)
            
            if hist_resp.status_code != 200:
                # This means something went wrong.
                # I should raise a custom exception for this.
                logging.warn("You didn't receive a 200 code from Yahoo, you received a {}.".format(hist_resp.status_code))
                        
            bulk_response = hist_resp.json()['query']
            
            results_dict = bulk_response['results']
            
            quote_list = results_dict['quote']
            

            # This is a bit arbitrary but we want at least 50 days of trading in a stock to be available before we start tracking trends.
            if len(quote_list) >= 50:       
            
                my_stock = Security(quote_list)
                up_signal_generated = False
                down_signal_generated = False
                
                ten_day_sma = my_stock.get_10_day_sma()
                twenty_day_ema = my_stock.get_20_day_ema()
                thirty_day_ema = my_stock.get_30_day_ema()

                
                # Check for up-trend
                if ten_day_sma > twenty_day_ema or ten_day_sma > thirty_day_ema: up_signal_generated = True
                
                # Check for down-trend
                if ten_day_sma < twenty_day_ema or ten_day_sma < thirty_day_ema: down_signal_generated = True
                    
                # Open a connection to our Dynamodb table for current trends.
                
                # For local development.
                #dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
                
                # For running against our AWS instance.
                dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://dynamodb.us-east-1.amazonaws.com")
                
                current_trend_table = dynamodb.Table('Current_Trend')             
                
                # Open a connection to the trend_history_table.
                trend_history_table = dynamodb.Table('Trend_History') 
                
                if up_signal_generated: 
                    logging.info("We have a up-trend signal from {}".format(k))
                    # Check if the stock has a stored up-trend.  If so, then ignore. 
                    # The response comes in the form of a dictionary object.  If it has length of 1 then the symbol was not previously saved.
                    # If it has more than one, then you are getting a response from the database and there is a current trend saved.
                    
                    response = current_trend_table.get_item(Key={'stock_symbol': k})
                    if len(response) == 1:
                        # Save the trend to the db.
                        logging.info("Saving trend to the db")
                        if save_up_trend(k, True) == 1: tally_notification(k, 'up')
                        else: logging.warn("We were unable to save the up-trend for {}".format(k))
                        
                    elif len(response) > 1:
                        # Check if the stock is already on an uptrend, if it is, then just move on.  
                        # If it isn't, then update the entry to indicate up-trend = True, and down-trend = False.
                        # 'Item': {'trend_start_date': '2016-07-06', 'up-trend': False, 'stock_symbol': 'AMD', 'down-trend': True}}
                        #trend_info = 
                        if response['Item']['up_trend'] == True: logging.info("We already know about the up-trend for {}".format(k)) # We are literally passing here, we already know about the up-trend.
                        elif response['Item']['up_trend'] == False:
                            # Updating trend in the database.
                            if save_up_trend(k, True) == 1: tally_notification(k, 'up') 
                            else: logging.warn("We were unable to save the new up-trend for {}".format(k))
                elif down_signal_generated: 
                    logging.info("We have a down-trend signal from {}".format(k))
                    # When a down-trend occurs we check if the stock has a stored down-trend. 
                    # If so, we ignore, if not, then update the down-trend bit to true, update the up-trend bit to false, insert the date, then notify.
                    response = current_trend_table.get_item(Key={'stock_symbol': k})
                    if len(response) == 1:
                        # Save the trend to the db as this is a either a new signal or a new stock.
                        logging.info("Saving new trend to the db")
                        if save_down_trend(k, True) == 1: tally_notification(k, 'down') 
                        else: logging.warn("We were unable to save the down-trend for {}".format(k))
                        
                    elif len(response) > 1:
                        # Check if the stock is already on a downtrend, if it is, then just move on.  
                        # If it isn't, then update the entry to indicate down_trend = True, and up-trend = False.
                        # 'Item': {'trend_start_date': '2016-07-06', 'up-trend': False, 'stock_symbol': 'AMD', 'down-trend': True}}
                        if response['Item']['down_trend'] == True: logging.info("We already know about the down-trend for {}".format(k)) # We are literally passing here, we already know about the down-trend.
                        elif response['Item']['down_trend'] == False:
                            # Updating trend in the database.
                            if save_down_trend(k, False) == 1: tally_notification(k, 'down')
                            else: logging.warn("We were unable to save the new down-trend for {}".format(k))        
                else:
                    logging.info("No trend detected for {} which means the SMA and EMA are equal".format(k))
                
                
                logging.info("Current 10 day SMA is {}, current 20 day EMA is {}, and current 30 day EMA is {}".format(my_stock.get_10_day_sma(), my_stock.get_20_day_ema(),my_stock.get_30_day_ema()))
                
               
            else: logging.info("This stock has not been traded long enough to do analysis on it.")
        except TypeError: logging.info("Came back with a TypeError from Yahoo Finance.")    # This is the error that is thrown if the query to Yahoo comes back with nothing.  Sometimes it happens with a bad stock symbol.
        except IndexError: logging.info("Somehow we got a stock through that didn't have enough entries.")
        logging.info("-----------------End work on stock symbol {} at {}.------------------------".format(k, datetime.datetime.today()))
    logging.info(len(notification_dict))
    
    if len(notification_dict) > 0:
        for j in notification_dict.keys():
            logging.info("You have new {} trend for {}".format(notification_dict[j], j))
    else: logging.info("No new trend notifications today.")
    
    logging.info("All Done at {}.".format(datetime.datetime.today()))

    
    




if __name__ == "__main__": main()