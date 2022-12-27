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

* b) While creating the Lambda Function, set up the IAM role for the lambda function On AWS, IAM stands for Identity Access Management. and is used to define roles and policies that different users/services can assume within your cloud infrastructure. It helps with managing secure access to services. Read/write access and scope can be configured on a defined role and also be re-used across similar workflows on the AWS cloud. Below we call it lambdas3ReadRole.
![alt text](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/lambda_images/lambda_Set_Up_2_permissions.png)

* #### c) Copy the script from the **_[1st_lambda_function.py](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/lambda_images/1st_lambda_function.py)_** file on this github repository and paste it within that of your newly created lambda function. Remember to edit your aws_access_key_id and aws_secret_access_key.

![alt text](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/lambda_images/lambda_Set_Up_4_permissions.png)

* #### d) In the Next 5 steps, we would modify the policy for the role we created for our Lambda function to also allow Lambda access to write to s3. Note that Failure to do this will result in an 'Access Denied Error' as seen **_[here](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/CloudWatch/CloudwatchErrors.png)_**


* #### i] ![alt text](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/lambda_images/lambda_Set_Up_5_policy.png)

* #### ii] ![alt text](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/lambda_images/lambda_Set_Up_6b_policy.png)

* #### iii] ![alt text](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/lambda_images/lambda_Set_Up_7_policy.png)

* #### iv] ![alt text](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/lambda_images/lambda_Set_Up_8_policy.png)

* #### v] ![alt text](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/lambda_images/lambda_Set_Up_9_policy.png)

* #### vi] ![alt text](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/lambda_images/lambda_Set_Up_10_policy.png)

* #### vii] ![alt text](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/lambda_images/lambda_Set_Up_11_policy_attachment.png)

* #### viii] Lastly review the policy to be sure it is in order.
 ![alt text](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/lambda_images/lambda_Set_Up_12_policy_Review.png)

For our Lambda Function to run properly, we would need to import the pandas and Scrape Shopify library in a layer. This is because, by default, the pandas library does not come with the python 3.8 runtime on AWS. Below is a sample of Runtime error we would encounter if we tried to run our lambda function before adding the virtual environment layer contaning pandas.

* #### ix] ![alt text](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/lambda_images/lambda_Set_Up_13_layerError.png)


While we can import this environment layer as a zipfile, To easily package this layer on AWS, we can run some commands on **_[Cloud9](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/Cloud9/Cloud9)_** against an EC-2 Instance.

### STEP 3 : Package Python virtual environment as a Layer with Cloud9 interface on an EC2 Instance.

Navigate back to your console, and search for cloud9 and follw the steps in the images below.

* #### i] ![alt text](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/Cloud9/Cloud9_Set_Up1.png)

* #### ii] ![alt text](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/Cloud9/Cloud9_Set_Up2.png)

* #### iii] ![alt text](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/Cloud9/Cloud9_Set_Up3.png)

* #### iv] ![alt text](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/Cloud9/Cloud9_Set_Up4.png)

* v] Once you are done with the tasks above , click on 'Open IDE' to open up the command session of your EC-2 instance where you can now run your commands.

* vi ] Next, run the commands outlined in the **_[Cloud9](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/Cloud9/Cloud9)_** file within the github repository. Copy and run them line by line.

* vii ] After the above execution , this layer should now be accessible to our Lambda Function.  

### STEP 4 - ADD Layer to LAMBDA Function

In this step we would add the Layer created in Step 3 above to our Lambda Function. To do this, follow the images below;  

* i ] On your Lambda Function Page, Scroll down to the Layer Section. 
![alt text](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/lambda_images/lambda_Set_Up_21_layer.png)

* ii ] ![alt text](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/lambda_images/lambda_Set_Up_22_layer.png)


* iii ] ![alt text](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/lambda_images/lambda_Set_Up_23_layer.png)


### STEP 5 - ADD EventBridge to Trigger the Lambda on a daily basis (Cron Job)

For this Lambda Function to be triggered on a daily basis, we will need to use EventBridge as a trigger for this task. 

* i] ![alt text](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/EventBridge/EventBridge0.JPG)

* ii] ![alt text](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/EventBridge/EventBridge1.JPG)


### STEP 6 - Create another S3 bucket.

This bucket will be the destination or target where the file we will processed will be stored. Use the first step for this. The reason we will do this by not just creating another directory or folder is to avoid bucker recursion. We will name the bucket processed and a sub folder /processed.


### STEP 7 - Create another Lambda Function
We are going to create a new Lambda function that will be triggered to transform the file we have scrapped. Use ### Step 2 for this with this **_python_script(https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/transform_load.py)_**. 

### N/B: Also, remember to add a policy to be able to read the from the ealier s3 bucket which we created. 


### STEP 8 - Add s3 Trigger for Lambda

For Lambda to be triggered when an event occurs in s3, we need to add a new s3 trigger to this Lambda. In this case, we are interested in Put Events. Follow the steps below;

* i] Click on Add Trigger
  ![alt text](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/EventBridge/EventBridge0.JPG)

* ii] On the bucket option, select the bucket that we first created ( this is the bucket that will trigger the Lambda fuction when a file lands). For EVENT TYPE, select PUT and put the folder path ie raw/ in the Prefix. 
* 
  ![image](https://user-images.githubusercontent.com/46321827/207144222-03c85e26-699a-4b41-9929-ed29fc4b4176.png)

### STEP 9 - Set Up SNS Notification

In Order for us to receive Mail alerts when our file is processed, we would create an SNS Topic to do this for us. On your Console, search for SNS and Follow the steps in the images below;

* i] Create a topic with any name and description, then proceed to set up an Access Policy for the Topic. 

  ![alt text](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/SNS/SNSTopic_1.png)

* ii]  ![alt text](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/SNS/SNSTopic_2.png)


* iii]  ![alt text](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/SNS/SNSTopic_3.png)


* iv] Immediately after the subscription above , navigate to your inbox to find a mail that looks like the one shown below. Click Confirm. 

![alt text](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/SNS/SNSTopic_4.png)


* v] After confirmation, you should see a page that looks like the one shown below.   
![alt text](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/SNS/SNSTopic_5.png)


* vi] When you go back to the SNS Console, you should now see the confirmed status on that subscription. It should look similar to the image shown below. 
![alt text](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/SNS/SNSTopic_6.png)


### EXECUTION

With everything now set up, we can go ahead to run our first Lambda Function to see how the data is loaded into our first s3 bucket. Follow the steps below to see the Magic afterwards !! ..
  ### 1. a] Navigate to the first Lambda and run it.
  
![alt text](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/observation/obs1.JPG)

 ### b] Go to s3 and check the first bucket(raw) we created
  
![alt text](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/observation/obs3.JPG)

 As we can see the file has now been loaded into the folder and then this will trigger the 2nd Lambda which will process the file and load into the processed bucket. 
 
### c] Check the processed bucket to see if the file is there. This is the final checking stage. 

![alt text](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/observation/obs4.JPG)
 
 
 ### CLOSING NOTES

    * Congratulations on Successfully completing this project on AWS. Amazon Web Services like other major cloud providers, gives an array of cloud computing services which can greatly increase efficiency of engineering teams within any establishment.

    * You might have run into errors while executing this project, That is part of the learning/implementation journey. Do well to check out AWS Community pages /Faq pages for solutions to your errors. You can also contact me via Linkedin @silas-ugorji.

    * Depending on your Use Case for similar operations, AWS advices that you use two different s3 buckets to avoid conflicts during transactions within one bucket.

    * In the course of developing this project, this **_[video] (https://www.youtube.com/watch?v=H_rRlnSw_5s&feature=youtu.be)_** from Be A Better Dev on Youtube was helpful. You can check it out.

    * If you are not using this in production, Remember to delete the resources you used for this project to avoid encountering unprecedented bills. In my case, i used these services on the Free Tier provided by AWS, hence my bill was $0 as seen here.
