# Scania trucks Sensor fault detection

## Overview

The project is an end-to-end machine learning application designed to explore the Scania trucks dataset, comprising of sensor data from the trucks, select the best model, and deploy and build a CI/CD pipeline with it.

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

- The model is deployed on AWS ECS with CircleCI as an AIOps agent.

### Deployment Process

- (Briefly explain the deployment steps and any configurations)

## Future Improvements

- Usage of AWS load balancer to pertain a single Public IP

## Contact Information

- Email: svkadhikary7@gmail.com
- LinkedIN: https://www.linkedin.com/in/svk-adhikary/

