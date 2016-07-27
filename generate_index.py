#!/usr/bin/python

import boto3

def main():
    # We will connect to S3, pull the list of files and generate an index.html file with a list of hyperlinks then copy that file to the rodell.info S3 bucket.
    
    #client = boto3.client('s3', 'us-east-1')
    
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('rodell.info')
    
    # Now we write out our results sorted on volume and price ranges. 
    results_file_name = "list.html"
    results_file = open(results_file_name, 'w')
    
    print("""<!DOCTYPE html>
        <html lang="en">
        <head>
        <title>
        Results List:\n
        </title>
        </head> 
        <body>
        <h2> Following are our results files: </h2>""", file=results_file)
    
    #if len(bucket.objects.all()) > 0:  
    # First we loop through and notify on our indices.
    print("<ul>", file=results_file)
    for key in bucket.objects.all():
        if key.key.find("result") != -1: print("<li><a href='{}'>{}</a></li>".format(key.key, key.key), file=results_file)
    print("</ul>", file=results_file)
        
        
    #else: print("<p>There are no results files.", file=results_file)
    
    print("</body>\n</html>", file=results_file)
    results_file.close()
    
    bucket.upload_file(results_file_name, results_file_name, ExtraArgs={'ContentType': 'text/html'})
        
if __name__ == "__main__": main()