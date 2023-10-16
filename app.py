import os
import time
import streamlit as st
from sensor.pipeline.training_pipeline import TrainingPipeline
from sensor.pipeline.batch_prediction import SensorBatchPrediction
from sensor.entity.config_entity import TrainingPipelineConfig, BatchPredictionConfig
from upload_data import storing_data_in_mongo


st.title("Sensor Data Machine Learning Workflow")
def start():
    st.text("You can start now")

st.button("Click this button first", on_click=start)
st.text("The above button is to avoid streamlit's Widget state reset behaviour")
# Upload training data in Mongo 
# Add a text input field to enter the file path
upload_file = st.file_uploader("Enter file path to upload to DB:")
upload_file_path = os.path.join("data", "upload_file")
try:
    if upload_file is not None:
        if not os.path.exists(upload_file_path):
            os.makedirs(upload_file_path)
        with open(os.path.join(upload_file_path, "upload_file.csv"), "wb") as f:
            f.write(upload_file.getbuffer())
        st.success("Press upload to upload the data in database")        
except Exception as e:
    st.error(str(e))

if st.button("Upload Data"):
    try:
        if os.path.exists(upload_file_path):
            upload_file_path = upload_file_path + "/" + "upload_file.csv"
            storing_data_in_mongo(upload_file_path)
            st.success("Data successfully stored in Database")
        else:
            st.error("File path does not exists")
    except Exception as e:
        st.error(f"Exception occurred: {str(e)}")

# Train on uploaded data in mongodb
def train():
    try:
        training_pipeline_config = TrainingPipelineConfig()
        training_pipeline = TrainingPipeline(training_pipeline_config)
        with st.status("Training in progress, don't click any buttons", expanded=True) as status:
            st.write("Ingesting data")
            data_ingestion_artifact = training_pipeline.start_data_ingestion()
            status.success("Data imported successfully")
            st.write("Validating data")
            data_validation_artifact = training_pipeline.start_data_validation(data_ingestion_artifact)
            status.success("Data validated")
            st.write("Transforming data")
            data_transformation_artifact = training_pipeline.start_data_transformation(data_validation_artifact)
            status.success("Data transformed")
            st.write("Model Training started")
            model_trainer_artifact = training_pipeline.start_model_trainer(data_transformation_artifact)
            status.success("Model training successful")
            st.write("Evaluating Model")
            model_evaluation_artifact = training_pipeline.start_model_evaluation(data_validation_artifact=data_validation_artifact,
                                                                    data_transformation_artifact=data_transformation_artifact,
                                                                    model_trainer_artifact=model_trainer_artifact)
            status.success("Model evaluation complete")
            st.write("Pushing model to production")
            model_pusher_artifact = training_pipeline.start_model_pusher(data_transformation_artifact=data_transformation_artifact,
                                                            model_trainer_artifact=model_trainer_artifact)
            status.success(f"Model saved at {model_pusher_artifact.saved_model_dir}")
        st.success("Training Completed, Success")
    except Exception as e:
        st.exception(f"An Exception occured: {str(e)}")

# predict on the uploaded file
train_button = st.button("Train", on_click=train, key="train_button")

# upload the file for prediction to inbox folder
predict_file = st.file_uploader("Upload file for prediction:")

# initialize batch prediction config
batch_pred_config = BatchPredictionConfig()

try:
    if predict_file is not None:
        inbox_dir = batch_pred_config.inbox_dir
        os.makedirs(inbox_dir, exist_ok=True)
        
        with open(os.path.join(inbox_dir, predict_file.name), "wb") as f:
            f.write(predict_file.getbuffer())
        st.success("File successfully uploaded, Tap predict to start prediction")
except Exception as e:
    st.error(e)

def predict():
    try:
        with st.spinner("Predicting data"):
            batch_pred_pipeline = SensorBatchPrediction(batch_pred_config)
            batch_pred_pipeline.start_prediction()
        st.success("Prediction saved in output folder")
    except Exception as e:
        st.exception(f"An exception occured: {str(e)}")

# predict on the uploaded file
predict_button = st.button("Predict", on_click=predict, key="predict")
    

