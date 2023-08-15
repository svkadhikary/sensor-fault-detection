from datetime import datetime
import os, sys
from sensor.exception import SensorException


TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"
TRANSFORMER_OBJECT_FILE_NAME = "transformer.pkl"
TARGET_ENCODER_OBJECT_FILE_NAME = "target_encoder.pkl"

class TrainingPipelineConfig:
    def __init__(self) -> None:
        try:
            timestamp = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
            self.artifact_dir = os.path.join('artifact', timestamp)
        except Exception as e:
            raise SensorException(e, sys)


class DataIngestionConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        try:
            data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir, "data_ingestion")
            self.dataset_dir = os.path.join(data_ingestion_dir, "dataset")
            self.train_file_path = os.path.join(self.dataset_dir, TRAIN_FILE_NAME)
            self.test_file_path = os.path.join(self.dataset_dir, TEST_FILE_NAME)
            self.database_name = "sensor"
            self.collection_name = "sensor_readings"
            self.test_size = 0.2
        except Exception as e:
            raise SensorException(e, sys)



class DataValidationConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig) -> None:
        try:
            data_vaildation_dir = os.path.join(training_pipeline_config.artifact_dir, "data_validation")
            self.valid_dir = os.path.join(data_vaildation_dir, "valid")
            self.invalid_dir = os.path.join(data_vaildation_dir, "invalid")
            self.valid_train_file_path = os.path.join(self.valid_dir, TRAIN_FILE_NAME)
            self.invalid_train_file_path = os.path.join(self.invalid_dir, TRAIN_FILE_NAME)
            self.valid_test_file_path = os.path.join(self.valid_dir, TEST_FILE_NAME)
            self.invalid_test_file_path = os.path.join(self.invalid_dir, TEST_FILE_NAME)
            self.report_file_name = os.path.join(data_vaildation_dir, "report", "report.yaml")
            self.schema_file_path = os.path.join("schema.yaml")
            self.missing_threshold = 0.7
        except Exception as e:
            raise SensorException(e, sys)

class DataTransformationConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig) -> None:
        try:
            self.transformation_dir = os.path.join(training_pipeline_config.artifact_dir, "data_transformation")
            self.transformer_obj_dir = os.path.join(self.transformation_dir, "transformer")
            self.transformer_obj_path = os.path.join(self.transformer_obj_dir, TRANSFORMER_OBJECT_FILE_NAME)
            self.target_encoder_obj_path = os.path.join(self.transformation_dir, "target_encoder", TARGET_ENCODER_OBJECT_FILE_NAME)
            self.transformed_data = os.path.join(self.transformation_dir, "transformed_data")
            self.transformed_train_path = os.path.join(self.transformed_data, TRAIN_FILE_NAME.replace("csv", "npz"))
            self.transformed_test_path = os.path.join(self.transformed_data, TEST_FILE_NAME.replace("csv", "npz"))
            self.schema_file_path = os.path.join("schema.yaml")
        except Exception as e:
            raise SensorException(e, sys)
        
        

