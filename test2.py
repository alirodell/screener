
import boto3



def main():
    
    #aws_ses = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://dynamodb.us-east-1.amazonaws.com")
    
    ses_client = boto3.client('ses', region_name='us-east-1')
    
    to_address= { 'ToAddresses': 'alirodell@gmail.com' }
     
    
    ses_client.send_email({'Source':'screener@rodell.info','ToAddresses':'alirodell@gmail.com', 'Subject':'Test email','Body':'This is a test body'})
            
    
if __name__ == "__main__": main()