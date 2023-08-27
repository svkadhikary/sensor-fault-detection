import os, sys
import pandas as pd
from sklearn.metrics import f1_score
from sensor.utils import load_object, read_yaml_file
from sensor.entity.config_entity import ModelEvaluationConfig
from sensor.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact, ModelTrainerArtifact, ModelEvaluationArtifact
from sensor.ml.model_resolver import ModelResolver
from sensor.exception import SensorException
from sensor.logger import logging


class ModelEvaluation:
    def __init__(self,
                 model_evaluation_config:ModelEvaluationConfig,
                 data_transformation_artifact:DataTransformationArtifact,
                 data_validation_artifact:DataValidationArtifact,
                 model_trainer_artifact:ModelTrainerArtifact
                 ) -> None:
        try:
            logging.info(f"{'=='*20}  Model Evaluation {'=='*20}")
            self.model_eval_config = model_evaluation_config
            self.data_transformation_artifact = data_transformation_artifact
            self.data_validation_artifact = data_validation_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.model_resolver = ModelResolver()
        except Exception as e:
            raise SensorException(e, sys)
        
    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        try:
            logging.info("Check if previously saved model is better than our current model")
            latest_dir_path = self.model_resolver.get_latest_dir_path()
            if latest_dir_path == None:
                model_eval_artifact = ModelEvaluationArtifact(is_model_accepted=True, improved_model_accuracy=None)
                logging.info(f"Model Evaluation Artifact: {model_eval_artifact}")
                return model_eval_artifact
            
            # if previous model available
            logging.info("Finding location and loading objects of previous tranformer, target encoder and model")
            transformer = load_object(self.model_resolver.get_latest_transformer_path())
            target_encoder = load_object(self.model_resolver.get_latest_target_encoder_path())
            model = load_object(self.model_resolver.get_latest_model_path())

            # Currently trained model
            logging.info("Loading currently trained model")
            current_transformer = load_object(self.data_transformation_artifact.transformer_object_path)
            current_target_encoder = load_object(self.data_transformation_artifact.target_encoder_path)
            current_model = load_object(self.model_trainer_artifact.model_file_path)

            # loading valid data
            logging.info("loading data to test models")
            test_df = pd.read_csv(self.data_validation_artifact.test_file_path)
            schema_info = read_yaml_file(self.model_eval_config.schema_file_path)
            target_col = schema_info['target_column']

            # transform target column
            target_df = test_df[target_col]
            y_true = target_encoder.transform(target_df)

            logging.info("Comparision between previous and curerntly trained model")
            # check prediction with previously trained model
            input_features = list(transformer.feature_names_in_)
            input_arr = transformer.transform(test_df[input_features])
            y_pred = model.predict(input_arr)
            logging.info(f"Prediction using previous model: {target_encoder.inverse_transform(y_pred[:5])}")
            prev_model_score = f1_score(y_true, y_pred)
            logging.info(f"Accuracy score using previous model: {prev_model_score}")

            # check prediction with current model
            y_true = current_target_encoder.transform(target_df)
            input_features = list(current_transformer.feature_names_in_)
            input_arr = current_transformer.transform(test_df[input_features])
            y_pred = current_model.predict(input_arr)
            logging.info(f"Prediction using Current model: {current_target_encoder.inverse_transform(y_pred[:5])}")
            current_model_score = f1_score(y_true, y_pred)
            logging.info(f"Accuracy score using current model: {prev_model_score}")

            # check the accuracy difference
            diff = current_model_score - prev_model_score
            if diff < self.model_eval_config.change_threshold:
                logging.info("Currently trained model is not better than the previous model")
                raise Exception("Current trained model is not better than the previous model")
            
            # model evaluation artifact
            model_eval_artifact = ModelEvaluationArtifact(
                improved_model_accuracy=diff,
                is_model_accepted=True
            )
            logging.info(f"Model Evaluation Artifact: {model_eval_artifact}")
            
            return model_eval_artifact

        except Exception as e:
            raise SensorException(e, sys)

