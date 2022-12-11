# AWS S3 EVENT TRIGGERED LAMBDA FUNCTION, EVENTBRIDGE, AND SNS NOTIFICATION

**_[Author: Silas Ugorji](https://www.linkedin.com/in/silas-ugorji/)_**

**Date: 08/12/2022**

## Project Architecture
The Workflow of this project is shown below depicting how the following AWS solutions are used and can aid your data engineering processes. AWS provides cloud serveless computing solutions like Lambda & Glue, and storage services like s3 - (Simple Storage Service) alongside an array of pay-as-you-go services that are cheap and affordable. Some of the ones used in this project are S3, Lambda, Event Bridge, SNS, and Cloud9.


![alt text](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/AWS_S3_Project.png?raw=true)

## About The Project
This project demonstrates a simple use-case for data gathering(web-scraping), Storage, transformation, and automation of this process. Sometimes, as part of an ETL/ELT process of data engineering, we save raw data from apps, scrapped data, etc to your data lake in an unprocessed format (bronze form) and then begin downstream processing to either silver format or even a usable format for analytics like loading to an RDBMS (Relational Database Management System) or using Athena to analyze the data. However, on some occasions you may want the following ;

* Scrape or gather the data from one or more sources.
* If the process would be recurrent, you may want to make it fully automated.
* Trigger one event after another.
* to get notifications when a task is complete/ encounters a failure.

In the first stage of the above workflow, we will use a python script to scrape products from a Shopify website and load the data into an S3 bucket in CSV format. The script is the **_[scrape_shopify.py](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/scrape_data.py)_** file. The automation is as follows;
### Stage one

* Scrape the data from the Shopify website of your choice, using **_[scrape_shopify.py](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/scrape_data.py)_** file and dumping it into our target S3 bucket.
* Automate the above using a Lambda function which will be triggered every morning using AWS EventBridge.
* N/B: Lambda is a serverless computing solution that can run your workloads. It can use either a python or node.js runtime as at the time of this writing. So in this case we have a python script running on Lambda to scrape the website and load the data into an S3 raw layer or zone.
* N/B: EventBridge Scheduler is a serverless scheduler that allows you to create, run, and manage tasks from one central, managed service. In this project, we will use it for CRON job which will trigger the Lambda function to run every day at 6 am.

### Stage two

* Immediately a file arrives in the raw zone of your s3 bucket (data lake).
An S3 Put event is Triggered and subsequently makes a call to another Lambda function. The Lambda function will run this **_[process_data.py](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation)_** file.

* Lastly once a transaction stream is processed and written to the processed zone of our s3 bucket, we want our s3 bucket put-event to also trigger an email using SNS (Simple Notification Service) to let us know some details about the workload like runtime, and some metadata of what was put into the s3 bucket.
* N/B: SNS helps us create Topics that users can subscribe to in order to able to receive simple notifications on events. This can be either by email or SMS.

We also want to be able to check our logs using Cloudwatch.
* N/B: Cloudwatch is a monitoring and observability service that helps us monitor applications/infrastructure on AWS. In simple terms, this service allows us to see logs for events used on AWS. Each log is stored with a corresponding timestamp for easy tracking.

### Prerequisites

- An AWS account (Free)
- Basic Understanding of the above workflow and what we are trying to achieve
- 1st Lambda code for getting data in `scrape_shopify.py` - from the repository
- 2nd Lambda code for transforming the data in the raw zone in 'process_data.py' - from the repository


## LET'S PROCEED

### STEP 1 - Set Up an AWS S3 Bucket with one object(folder) raw.
Go to your AWS console and search for S3 follow the steps in the image below.
* #### a)

![alt text](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/s3-files/S3_Bucket_1.png)

* #### b) Give your bucket a name and leave the default settings and click create a bucket.
![alt text](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/s3-files/s3-2.JPG)

* #### c) Create the raw folder which will be the landing zone for the scrapped CSV file using Lambda.
![alt text](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/s3-files/s3-3.JPG)

### STEP 2 - Set up the first Lambda Function

Now let us set up our 1st lambda function which is going to be at the heart of our data scraping from the target website. This Function would scrape the Shopify website using the Shopify module. We will use a pandas dataframe (in memory) and subsequently write it to the /raw directory of our s3 bucket. On your console, search for Lambda and follow the steps below.

* #### a) Give your function a Name and select Python 3.8 as the runtime
![alt text](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/lambda_images/lambda_Set_Up_1_permissions.png)

* #### b)
 While creating the Lambda Function, set up the IAM role for the lambda function On AWS, IAM stands for Identity Access Management. and is used to define roles and policies that different users/services can assume within your cloud infrastructure. It helps with managing secure access to services. Read/write access and scope can be configured on a defined role and also be re-used across similar workflows on the AWS cloud. Below we call it lambdas3ReadRole .
-- 

* #### c) Copy the script from the **_[1st_lambda_function.py](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/lambda_images/1st_lambda_function.py)_** file on this github repository and paste it within that of your newly created lambda function. Remember to edit your aws_access_key_id and aws_secret_access_key.





