import os
import sys
import numpy as np
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.config_entity import DataIngestionConfig
from sensor.entity.artifact_entity import DataIngestionArtifact
from sensor.utils import export_collection_as_dataframe



class DataIngestion:

    def __init__(self, data_ingestion_config:DataIngestionConfig) -> None:
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise SensorException(e, sys)
        

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info(f"Exporting collection as dataframe")
            df = export_collection_as_dataframe(
                database_name=self.data_ingestion_config.database_name,
                collection_name=self.data_ingestion_config.collection_name
                )
            # correct missing value format
            logging.info(f"Replacing missing value na with NAN")
            df.replace({'na':np.NAN}, inplace=True)
            # split into train and test df
            logging.info(f"Splitting dataset into train and test")
            train_df, test_df = train_test_split(df, test_size=self.data_ingestion_config.test_size, random_state=42)
            # create dataset directory if not exists
            logging.info(f"Creating dataset directory")
            os.makedirs(self.data_ingestion_config.dataset_dir, exist_ok=True)
            # save train and test csv
            logging.info(f"Saving train and test csv")
            train_df.to_csv(self.data_ingestion_config.train_file_path, index=False, header=True)
            test_df.to_csv(self.data_ingestion_config.test_file_path, index=False, header=True)
            
            logging.info(f"Preparing data ingestion artifact")
            data_ingestion_artifact = DataIngestionArtifact(
                self.data_ingestion_config.train_file_path,
                self.data_ingestion_config.test_file_path
            )

            logging.info(f"Data Ingestion Artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact

        except Exception as e:
            raise SensorException(e, sys)

