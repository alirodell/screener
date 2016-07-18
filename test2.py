
import boto3
import datetime




def main():
    
    end_date = datetime.date.today() - datetime.timedelta(hours=24)
    print(end_date)
    # Start date is represented by @@@@ in the url.
    # Go back 100 calendar days which should give us around 70 trading days.
    start_date = end_date - datetime.timedelta(days=300)
    print(start_date)
    today_date_string = str(end_date) 
    
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://dynamodb.us-east-1.amazonaws.com")


    current_trend_table = dynamodb.Table('Current_Trend')             
                    
    # Open a connection to the trend_history_table.
    trend_history_table = dynamodb.Table('Trend_History') 
    
    response = current_trend_table.get_item(
        Key={
            'stock_symbol': 'CZR'
        }
    )
    
    print(response)
    
    print(trend_history_table.get_item(
        Key={
            'stock_symbol': 'CZR',
            'occurence_date': '2016-07-11'
        }
    ))
    
    #aws_ses = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://dynamodb.us-east-1.amazonaws.com")
    
    #ses_client = boto3.client('ses', region_name='us-east-1')
    
    #to_address= { 'ToAddresses': 'alirodell@gmail.com' }
     
    
    #ses_client.send_email({'Source':'screener@rodell.info','ToAddresses':'alirodell@gmail.com', 'Subject':'Test email','Body':'This is a test body'})
            
    
if __name__ == "__main__": main()