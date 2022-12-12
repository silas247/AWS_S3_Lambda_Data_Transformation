import json
import pandas as pd
import boto3
import secrets
from io import StringIO
from datetime import datetime as dt

year = dt.now().year
month = dt.strftime(dt.now(), '%B')
day = dt.now().day
hour = dt.now().hour
min = dt.now().minute

def lambda_handler(event, context):
   ##"""Accessing the S3 buckets using boto3 client"""
    s3_client =boto3.client('s3')
    s3_resource = boto3.resource('s3')
    s3_bucket_name='nagative-raw-zone'
    s3 = boto3.resource('s3',
                        aws_access_key_id= 'Put yours',
                        aws_secret_access_key='Put yours)
        
        
    my_bucket = s3.Bucket(s3_bucket_name) #bucket name
    ##
    for f in my_bucket.objects.filter(Prefix = 'raw/'): ## looping throught the S3 directory to find the latest file using the day of the file.
        file_name = f.key
        if file_name.find(f"nagative-raw-zone_{year}_{month}_{day}")!=-1: #getting the latest csv file we are interested in. 
            # print(file_name)
            obj2 = s3_client.get_object(Bucket=  s3_bucket_name, Key= file_name) 
            df = pd.read_csv(obj2['Body']) # reading the data 
            #print(df)
    #Transform the data to Pick the columns needed and then rename them 
    df1 = df[['product_id','parent_title','available','grams','price','taxable','created_at','updated_at','vendor']]
    df1.columns = ['Product_Id','Product_Name','Products','Weight_grams','Price','Taxable','Date_Created','Updated_date','Vendor']
    #print(df1)
        
    # s3_client =boto3.client('s3')
    # s3_resource = boto3.resource('s3')
    s3_bucket_name2='nagative-processed-zone'
    # s3 = boto3.resource('s3',
    #                     aws_access_key_id= 'AKIAQYDWQQBAFTLSIV5X',
    #                     aws_secret_access_key='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')    
        
    
    
      
    #write to buffer memory
    csv_buffer = StringIO()
    #convert df1 to csv
    df1.to_csv(csv_buffer)
    #write to the S3 processed zone
    s3_resource.Object(s3_bucket_name2, f"processed/nagative-processed-zone_{year}_{month}_{day}_{hour}_{min}.csv").put(Body=csv_buffer.getvalue())
           
    #    return "Job Done"
    
