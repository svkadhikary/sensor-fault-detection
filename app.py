import os
import streamlit as st
from sensor.pipeline.training_pipeline import TrainingPipeline
from sensor.pipeline.batch_prediction import SensorBatchPrediction
from sensor.entity.config_entity import TrainingPipelineConfig, BatchPredictionConfig
from upload_data import storing_data_in_mongo
from sensor.logger import logging


st.title("Sensor Data Machine Learning Workflow")

# Upload training data in Mongo 
# Add a text input field to enter the file path
file_path = st.text_input("Enter file path:")
if st.button("Upload Data"):
    try:
        if os.path.exists(file_path):
            storing_data_in_mongo(file_path)
        else:
            st.error("File path does not exists")
    except Exception as e:
        st.error(f"Exception occurred: {str(e)}")

# Train on uploaded data in mongodb
if st.button("Train"):
    try:
        training_pipeline_config = TrainingPipelineConfig()
        training_pipeline = TrainingPipeline(training_pipeline_config)
        training_pipeline.start()
        st.write("Training Completed, Success")
    except Exception as e:
        st.exception(f"An Exception occured: {str(e)}")

if st.button("Predict"):
    try:
        batch_pred_config = BatchPredictionConfig()
        batch_pred_pipeline = SensorBatchPrediction(batch_pred_config)
        batch_pred_pipeline.start_prediction()
        st.write("Prediction saved in output folder")
    except Exception as e:
        st.exception(f"An exception occured: {str(e)}")

