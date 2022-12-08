# DEMO PROJECT ON AWS S3 EVENT TRIGGERED LAMBDA FUNCTION, EVENT BRIDGE AND SNS NOTIFICATION

**_[Author: Silas Ugorji](https://www.linkedin.com/in/silas-ugorji/)_**

**Date:08/12/2022**

## Project Architecture
The Workflow of this project is shown below depicting how the following AWS solutions are used and can aid your      data engineering processes. AWS provides cloud serveless compute solutions like Lambda & Glue, storage services      like s3 - (Simple Storage Service) alongside an array of pay-as-you-go services which are cheap and affordable.      Some of the ones used in this project are S3, Lambda, Event Bridge, SNS and Cloud9.


![alt text](https://github.com/silas247/AWS_S3_Lambda_Data_Transformation/blob/main/AWS_S3_Project.png?raw=true)

## About The Project
This project demonstrates a simple usecase for data gathering(web-scraping), Storage, transformation and automation of this process. Sometimes, as part of an ETL/ELT process of data engineering, we save raw data from apps,scrapped data, etc to your data lake in an unprocessed format (bronze form) and then begin downstream processing to either silver format or even a usable format for analytics like loading to an RDBMS (Relational Database Management System) or using Athena to analyze the data. However, on some occassions you may want the following ;

    *If the process would be recurrent, you may want to make it fully automated.
    *Trigger one event after another
    *To get notifications when a task is complete/ encounters a failure.
