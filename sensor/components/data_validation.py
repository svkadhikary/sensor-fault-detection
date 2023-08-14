import os, sys
from typing import Optional
import pandas as pd
import numpy as np
from scipy.stats import ks_2samp
from sensor.entity.config_entity import DataValidationConfig
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from sensor.utils import read_yaml_file, write_yaml_file
from sensor.logger import logging
from sensor.exception import SensorException


class DataValidation:

    def __init__(self,
                 data_validation_config:DataValidationConfig,
                 data_ingestion_artifact:DataIngestionArtifact
            ) -> None:
        try:
            logging.info(f"{'='*20} Data Validation {'='*20}")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.validation_error = dict()
        except Exception as e:
            raise SensorException(e, sys)

    def drop_missing_values_columns(self, df:pd.DataFrame, report_key_name:str)->Optional[pd.DataFrame]:
        try:
            threshold = self.data_validation_config.missing_threshold
            null_report = df.isna().sum()/df.shape[0]
            logging.info(f"Selecting the columns in the dataframe which contains null values above threshold {threshold}")
            drop_column_names = null_report[null_report>threshold].index
            logging.info(f"Columns to drop: {list(drop_column_names)}")
            self.validation_error[report_key_name] = list(drop_column_names)
            df.drop(list(drop_column_names), axis=1, inplace=True)

            if len(df.columns) == 0:
                return None
            return df

        except Exception as e:
            raise SensorException(e, sys)
    
    def is_required_column_exists(self, df:pd.DataFrame, report_key_name:str)->bool:
        try:
            schema_info = read_yaml_file(file_path=self.data_validation_config.schema_file_path)
            reqd_cols = schema_info['required_columns']
            logging.info(f"Required Columns: {reqd_cols}")
            missing_reqd_cols = []
            for col in reqd_cols:
                if col not in df.columns:
                    missing_reqd_cols.append(col)

            if len(missing_reqd_cols) == 0:
                return True
            
            logging.info(f"Missing required columns: {missing_reqd_cols}")
            self.validation_error[report_key_name] = missing_reqd_cols

        except Exception as e:
            raise SensorException(e, sys)
        
    def data_drift(self, base_df:pd.DataFrame, current_df:pd.DataFrame, report_key_name:str):
        try:
            drift_report = dict()
            base_cols = base_df.columns
            current_cols = current_df.columns
            for base_col in base_cols:
                base_data, current_data = base_df[base_col], current_df[base_col]
                logging.info(f"Hypothesis {base_col}: {base_data.dtype}, {current_data.dtype}")
                same_dist = ks_2samp(base_data, current_data)

                if same_dist.pvalue > 0.05:
                    # We accept null hypothesis
                    drift_report[base_col] = {
                        "p-values": float(same_dist.pvalue),
                        "same distribution": True
                    }
                else:
                    drift_report[base_col] = {
                        "p-values": float(same_dist.pvalue),
                        "same distribution": False
                    }
                    # different distribution
                
            self.validation_error[report_key_name] = drift_report
            
        except Exception as e:
            raise SensorException(e, sys)
        
    def drop_columns(self, df:pd.DataFrame)->pd.DataFrame:
        try:
            schema_info = read_yaml_file(self.data_validation_config.schema_file_path)
            drop_cols = schema_info["drop_columns"]
            logging.info(f"Dropping columns based on schema provided: {drop_cols}")
            df.drop(list(drop_cols), axis=1, inplace=True)
            return df
        
        except Exception as e:
            raise SensorException(e, sys)
        
    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            train_df = self.drop_columns(df=train_df)
            test_df = self.drop_columns(df=test_df)

            train_df = self.drop_missing_values_columns(train_df, report_key_name='train_missing_values_columns')
            test_df = self.drop_missing_values_columns(test_df, report_key_name='test_missing_values_columns')

            if train_df is None:
                logging.info(f"No columns left in train df. Stopping pipeline")
                raise Exception("No columns left in train df. Stopping pipeline")
            
            if test_df is None:
                logging.info(f"No columns left in test df. Stopping pipeline")
                raise Exception("No columns left in test df. Stopping pipeline")
            
            is_exist = self.is_required_column_exists(df=train_df, report_key_name="train_required_column")

            if not is_exist:
                raise Exception("Required columns not available in train_df")
            
            is_exist = self.is_required_column_exists(df=test_df, report_key_name="test_required_column")

            if not is_exist:
                raise Exception("Required columns not available in test_df")
            
            if len(train_df.columns) != len(test_df.columns):
                raise Exception("Train and Test dataframe does not have equal number of columns")
            
            self.data_drift(base_df=train_df, current_df=test_df, report_key_name="train_test_drift_report")

            write_yaml_file(file_path=self.data_validation_config.report_file_name, data=self.validation_error)

            os.makedirs(self.data_validation_config.valid_dir, exist_ok=True)

            train_df.to_csv(self.data_validation_config.valid_train_file_path, header=True, index=False)
            test_df.to_csv(self.data_validation_config.valid_test_file_path, header=True, index=False)

            data_validation_artifact = DataValidationArtifact(
                report_file_path=self.data_validation_config.report_file_name,
                train_file_path=self.data_validation_config.valid_train_file_path,
                test_file_path=self.data_validation_config.valid_test_file_path,
                status=True
            )

            return data_validation_artifact

        except Exception as e:
            raise SensorException(e, sys)
