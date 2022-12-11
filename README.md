# AWS S3 EVENT TRIGGERED LAMBDA FUNCTION, EVENTBRIDGE AND SNS NOTIFICATION

**_[Author: Silas Ugorji](https://www.linkedin.com/in/silas-ugorji/)_**

**Date: 08/12/2022**

## Project Architecture
The Workflow of this project is shown below depicting how the following AWS solutions are used and can aid your      data engineering processes. AWS provides cloud serveless compute solutions like Lambda & Glue, storage services      like s3 - (Simple Storage Service) alongside an array of pay-as-you-go services which are cheap and affordable.      Some of the ones used in this project are S3, Lambda, Event Bridge, SNS and Cloud9.


![alt text](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/AWS_S3_Project.png?raw=true)

## About The Project
This project demonstrates a simple usecase for data gathering(web-scraping), Storage, transformation and automation of this process. Sometimes, as part of an ETL/ELT process of data engineering, we save raw data from apps,scrapped data, etc to your data lake in an unprocessed format (bronze form) and then begin downstream processing to either silver format or even a usable format for analytics like loading to an RDBMS (Relational Database Management System) or using Athena to analyze the data. However, on some occassions you may want the following ;

* Scrape or gather the data from one or more sources. 
* If the process would be recurrent, you may want to make it fully automated.
* Trigger one event after another.
* to get notifications when a task is complete/ encounters a failure.

In the first stage of the above workflow, we will be using a python script to scrape products from a Shopify website and load the data into an S3 bucket in csv format. The script is the **_[scrape_shopify.py](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/scrape_data.py)_** file. The automation is as follows;
### Stage one

* Scrape the data from the Shopify website of your choice, using **_[scrape_shopify.py](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/scrape_data.py)_** file and dumping it into our target S3 bucket.
* Automate the above using a Lambda function which will be triggered every morning using AWS EventBridge. 
    * N/B: Lambda is a serveless compute solution that can run your workloads . It can use either a python or node.js runtime as at the time of this writing. So in this case we have a python script running on Lambda to scrape the website and load the data into an S3 raw layer or zone. 
    * N/B: EventBridge Scheduler is a serverless scheduler that allows you to create, run, and manage tasks from one central, managed service. In this project, we will use it for CRON job which will trigger the Lambda function to run everyday at 6am.

### Stage two

* Immediately a file arrives the raw zone of your s3 bucket (data lake).
An S3 Put event is Triggered and subsequently makes a call to another Lambda function. The Lambda function will run this **_[process_data.py](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation)_** file.

* Lastly once a transaction stream is processed and written to the processed zone of our s3 bucket, we want our s3 bucket put event to also trigger an email using SNS (Simple Notification Service) to let us know some details about the workload like runtime, and some metadata of what was put into the s3 bucket.
   * N/B : SNS helps us create Topics that users can subscribe to in order to be able to receive simple notification on events. This can be either email or SMS.

   We also want to be able to check our logs using Cloudwatch.
   * N/B : Cloudwatch is a monitoring and observability service that helps us monitor applications/infrastructure on AWS. In simple terms, this service allows us to see logs for events used on AWS. Each log is stored with a corresponding timestamp for easy tracking.

### Prerequisites

   - An AWS account (Free)
   - Basic Understanding of the above workflow and what we are tring to achieve
   - 1st Lambda code for getting data in `scrape_shopify.py` - from repository
   - 2nd Lambda code for transforming the data in the raw zone in 'process_data.py'  - from       repository


## LET'S PROCEED

### STEP 1 - Set Up an AWS S3 Bucket with one object(folder) raw.
Go to your AWS console and search for S3 follow the steps in the image below.
   * ### a)

![alt text](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/s3-files/S3_Bucket_1.png)

