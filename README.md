# Scania trucks Sensor fault detection

## Overview

The project is an end-to-end machine learning application designed to explore the Scania trucks dataset, comprising of sensor data from the trucks, select the best model, and deploy and build a CI/CD pipeline with it.

## Dataset Description

The system in focus is the Air Pressure System (APS) which generates pressurized air that are utilized in various fuctions like braking, gear change etc. The dataset's positive class corresponds to component failures for a specific component of the APS system. The negative class corrsponds to the vehicles with failures for component not related to the APS system.

## Features

- **Dataset Analysis:** Comprehensive exploration of datasets to gain insights.
- **Model Selection:** Utilizing various ML libraries to identify the optimal model for classification tasks.
- **Deployment:** Deployment of the selected pipeline using Streamlit for a user-friendly web interface.

## Technologies Used

- **Programming Language:** Python 3.8
- **Web Interface:** Streamlit
- **Machine Learning Libraries:** Scikit-Learn, XGBClassifier, CatBoost, Imbalanced Learn, Pandas, Numpy, Scipy
- **Deployment Platform:** AWS ECS, AWS EFS, CircleCI

## Installation

### Instructions

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Export "MONGO_DB_URL:(your-mongo-db-database-connection-url)" variable as an environment variable.
4. Run with 'python app.py'.

OR

1. Clone the repository.
2. add the line ENV MONGO_DB_URL="(your-mongo-db-database-connection-url)" in Dockerfile
3. build a docker image and run.
4. For persisting data use docker run -v /(system_directory):/app/datadir -p 8501:8501 image/tag
   
## Usage
  
### Interacting with the Web Interface

The web interface has the functionality
- Upload data to database.
- Train an ML model with data available in the database.
- Make predictions by uploading data and save the predictions
- File explorer to explore and download the required dataset, model, artifacts, logs.

## Deployment

### Platform

- The model is deployed on AWS ECS with CircleCI as an MLOps agent.

### Deployment Process

- Build and push docker image manually at first
- Create role in AWS IAM user with AmazonECS_FullAccess policy enabled
    - Create Access Key for Command Line Interface access and download the access_key_id and security_access_key
- Create EFS volume for persistant storage
- Go Elastic Container Service
- Create cluster with cluster_name and select infrastructure AWS Fargate
- Create task definition
    - Write container_name, task_definition_family
    - Operating system: Linux X86_64
    - select CPU, RAM capacities
    - container port: 8501 (streamlit works on port 8501)
    - Image name is docker image_name:tag
    - Select Task role and Task execution role as ecsTaskExecutionRole
    - add environment variable like MongoDB URL
    - Add volume of type: EFS (for persistant storage)
    - Enter volume name, file system ID, root directory and access point ID as per EFS volume
    - Add mountpoint with container_name and path as /app/datadir
    - Create
- After creation directly click Deploy or go to previously created cluster and create service
    - Compute option: Capaity Provider Strategy
    - Family: task_definition_family; Revision: LATEST
    - Write a service_name
    - In network dropdown: create security group:- Type: All Traffic; Souce: Anywhere
    - Public IP turned on
    - Create
This will create the service and deploy the dockerized application.
Note down the Public IP from cluster_name --> Tasks --> click on the listed task.

## CI/CD
- After deploying the following strings are from the previous step
    - access_key_id
    - security_access_key
    - aws_region (The region where the container is deployed)
    - container_name
    - task_definition_family
    - image_name:tag
    - cluster_name
- Use this in circleci/config.yml file with the help of circleci_aws-ecs and circleci_aws-cli orbs
- Open CircleCI account, set up project from github, follow project
- The config file inside the .circleci/config.yml 
    - first sets up a virtual environment
    - builds and pushes new docker image to dockerhub
    - uses aws-cli to access aws using credetials
    - uses aws-ecs to deploy service update

- Setting this up triggers CircleCI whenever it notices an update in the project code in github, and automatically updates and deploys the ECS service with new image name updates.

## Future Improvements

- Usage of AWS load balancer to pertain a single Public IP

## Contact Information

- Email: svkadhikary7@gmail.com
- LinkedIN: https://www.linkedin.com/in/svk-adhikary/

