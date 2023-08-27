import os
import sys
import pandas as pd
import numpy as np
import json
import yaml
import dill
from .exception import SensorException
from .logger import logging
from .config import mongo_client

def dump_csv_to_mongodb(file_path:str, database_name:str, collection_name:str):
    try:
        # read data with pandas
        df = pd.read_csv(file_path)
        logging.info(f"Rows and columns shape: {df.shape}")
        # drop index column
        df.reset_index(drop=True, inplace=True)
        # convert to json
        json_records = list(json.loads(df.T.to_json()).values())
        # dump records in mongodb
        mongo_client[database_name][collection_name].insert_many(json_records)

    except Exception as e:
        raise SensorException(e, sys)
    
def export_collection_as_dataframe(database_name, collection_name)->pd.DataFrame:
    try:
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        if "_id" in df.columns:
            df.drop(['_id'], axis=1, inplace=True)

        return df
    except Exception as e:
        raise SensorException(e, sys)
    
def write_yaml_file(file_path, data:dict):
    try:
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir, exist_ok=True)
        with open(file_path, "w") as file_writer:
            yaml.dump(data,file_writer)
    except Exception as e:
        raise SensorException(e, sys)

def read_yaml_file(file_path):
    try:
        with open(file_path, "rb") as file_reader:
            return yaml.safe_load(file_reader)
    except Exception as e:
        raise SensorException(e, sys)

def save_object(file_path:str, obj:object):
    try:
        logging.info(f"Saving object")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
        logging.info(f"File object saved at {file_path}")
    except Exception as e:
        raise SensorException(e, sys)
    
def load_object(file_path: str, ) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not exists")
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise SensorException(e, sys) from e
    
def save_numpy_array_data(file_path:str, data:np.array):
    try:
        logging.info(f"Saving numpy array")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, data)
        logging.info(f"Numpy array saved at {file_path}")
    except Exception as e:
        raise SensorException(e, sys)
    
def load_numpy_array(file_path:str):
    try:
        logging.info(f"Loading numpy array: {file_path}")
        with open(file_path, "rb") as file_obj:
            data = np.load(file_obj)
        return data
    except Exception as e:
        raise SensorException(e, sys)