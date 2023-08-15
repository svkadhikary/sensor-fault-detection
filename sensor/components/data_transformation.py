import os, sys
from typing import Optional
import pandas as pd
import numpy as np
from sklearn.preprocessing import RobustScaler, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from imblearn.combine import SMOTETomek
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.utils import read_yaml_file, save_numpy_array_data, save_object
from sensor.entity.config_entity import DataTransformationConfig
from sensor.entity.artifact_entity import DataValidationArtifact, DataTransformationArtifact

class DataTransformation:
    def __init__(self, data_transformation_config:DataTransformationConfig,
                 data_validation_artifact:DataValidationArtifact) -> None:
        try:
            logging.info(f"{'==='*20}Data Transformation{'==='*20}")
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
        except Exception as e:
            raise SensorException(e, sys)
        
    def get_transformer_obj(self)-> Pipeline:
        try:
            simpleimputer = SimpleImputer(strategy='constant', fill_value=0)
            rb_scaler = RobustScaler()
            pipe = Pipeline(
                steps=[
                    ('Imputer', simpleimputer),
                    ('RobustScaler', rb_scaler)
                ]
            )
            return pipe
        except Exception as e:
            raise SensorException(e, sys)
    
    def get_target_encoder_obj(self)-> LabelEncoder:
        try:
            lbl_enc = LabelEncoder()
            return lbl_enc
        except Exception as e:
            raise SensorException(e, sys)
        
    def get_sampling_obj(self)-> SMOTETomek:
        try:
            return SMOTETomek(random_state=42)
        except Exception as e:
            raise SensorException(e, sys)
        
    def initiate_data_transformation(self)-> DataTransformationArtifact:
        try:
            schema_info = read_yaml_file(self.data_transformation_config.schema_file_path)
            target_column = schema_info['target_column']
            
            logging.info(f"Reading valid training and testing data")
            train_df = pd.read_csv(self.data_validation_artifact.train_file_path)
            test_df = pd.read_csv(self.data_validation_artifact.test_file_path)

            logging.info(f"Seperate input and target feature")
            input_feature_train_df=train_df.drop(target_column, axis=1)
            input_feature_test_df=test_df.drop(target_column, axis=1)
            target_feature_train_df = train_df[target_column]
            target_feature_test_df = test_df[target_column]

            logging.info(f"Converting target categorical column into numerical using label encoder")
            lbl_enc = self.get_target_encoder_obj()
            lbl_enc.fit(target_feature_train_df)
            target_feature_train_arr = lbl_enc.transform(target_feature_train_df)
            target_feature_test_arr = lbl_enc.transform(target_feature_test_df)

            logging.info(f"Transforming input features with simple imputer and robust scaler")
            transformation_pipe = self.get_transformer_obj()
            transformation_pipe.fit(input_feature_train_df)
            input_feature_train_arr = transformation_pipe.transform(input_feature_train_df)
            input_feature_test_arr = transformation_pipe.transform(input_feature_test_df)

            logging.info(f"Resampling dataset to handle imbalance")
            smt = self.get_sampling_obj()
            logging.info(f"Before resampling in training set, Input: {input_feature_train_arr.shape} Target:{target_feature_train_arr.shape}")
            input_feature_train_arr, target_feature_train_arr = smt.fit_resample(input_feature_train_arr, target_feature_train_arr)
            logging.info(f"After resampling in training set Input: {input_feature_train_arr.shape} Target:{target_feature_train_arr.shape}")
            
            logging.info(f"Before resampling in testing set Input: {input_feature_test_arr.shape} Target:{target_feature_test_arr.shape}")
            input_feature_test_arr, target_feature_test_arr = smt.fit_resample(input_feature_test_arr, target_feature_test_arr)
            logging.info(f"After resampling in testing set Input: {input_feature_test_arr.shape} Target:{target_feature_test_arr.shape}")

            # concat input and target array
            train_arr = np.c_[input_feature_train_arr, target_feature_train_arr]
            test_arr = np.c_[input_feature_test_arr, target_feature_test_arr]

            logging.info('saving the data')
            save_numpy_array_data(self.data_transformation_config.transformed_train_path, data=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_path, data=test_arr)

            logging.info("Saving transformer pipeline obj")
            save_object(self.data_transformation_config.transformer_obj_path, transformation_pipe)

            logging.info("Saving target encoder obj")
            save_object(self.data_transformation_config.target_encoder_obj_path, lbl_enc)

            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_path=self.data_transformation_config.transformed_train_path,
                transformed_test_path=self.data_transformation_config.transformed_test_path,
                transformer_object_path=self.data_transformation_config.transformer_obj_path,
                target_encoder_path=self.data_transformation_config.target_encoder_obj_path
            )

            return data_transformation_artifact

        except Exception as e:
            raise SensorException(e, sys)
    

