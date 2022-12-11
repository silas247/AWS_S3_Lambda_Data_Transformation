import json
from shopify_scraper import scraper
import pandas as pd
import boto3
import secrets
#from secrets import access_key, secret_access_key
from io import StringIO
from datetime import datetime as dt
def lambda_handler(event, context):
    #These dates variable will be appended at the end of the file name to make it unique
    year = dt.now().year
    month = dt.strftime(dt.now(), '%B')
    day = dt.now().day
    hour = dt.now().hour
    min = dt.now().minute
    
    
    #Url of the website to be scrapped.
    url = "https://negativeunderwear.com/"
    #This is the parent link which has a high level data of the products
    parents = scraper.get_products(url)
    #This is the child link with the  
    children = scraper.get_variants(parents)
    #Cpturing the children in a data frame
    df = pd.DataFrame(children)
    
    s3 = boto3.client('s3', aws_access_key_id=' Put your access key here', aws_secret_access_key='Put your access key here')
    bucket = 'nagative-raw-zone' # already created on S3
    
    #write to buffer memory
    csv_buffer = StringIO()
    df.to_csv(csv_buffer)
    
    #write to s3 folder
    s3_resource = boto3.resource('s3')
    s3_resource.Object(bucket, f"raw/negativeunderwear_products_{year}_{month}_{day}_{hour}_{min}.csv").put(Body=csv_buffer.getvalue())


    return {
        'statusCode': 200,
        'body': json.dumps('Job !')
    }
