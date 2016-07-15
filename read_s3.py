
import boto3
import datetime




def main():
    
    ##################################
    # Two buckets:
    #    1. rodell-screener-input
    #    2. rodell-screener-output
    #
    # Read the CSV files from the input bucket and upload log files and results to the output bucket.
    #
    # May decide to have the output bucket publicly available.
    ##################################
    
    results_file = 'results_2016-07-14.log'
    
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('rodell-screener-output')
    s3_file = bucket.Object('NASDAQ.csv')
    s3_file.download_file('NASDAQ.csv')

    s3.Object('rodell-screener-output', results_file).upload_file(results_file)        
    
if __name__ == "__main__": main()