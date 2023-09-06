import os
import sys
from sensor.utils import dump_csv_to_mongodb
from sensor.exception import SensorException
from sensor.logger import logging


def storing_data_in_mongo(file_path:str="E:/sensor_fault_detection/aps_failure_training_set1.csv"):
    try:
        database_name = "sensor"
        collection_name = "sensor_readings"
        logging.info(f"Uploading data to mongodb in database {database_name} collection {collection_name}")
        dump_csv_to_mongodb(file_path, database_name, collection_name)
    
    except Exception as e:
        raise SensorException(e, sys)
    

if __name__ == "__main__":
    storing_data_in_mongo()