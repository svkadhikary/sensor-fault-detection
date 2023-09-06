import os
import sys
from sensor.utils import dump_csv_to_mongodb
from sensor.exception import SensorException
from sensor.logger import logging


def storing_data_in_mongo():
    try:
        file_path = "E:/sensor_fault_detection/aps_failure_training_set1.csv"
        database_name = "sensor"
        collection_name = "sensor_readings"

        dump_csv_to_mongodb(file_path, database_name, collection_name)
    
    except Exception as e:
        raise SensorException(e, sys)

def test_exception_and_logger():
    try:
        x = 1/0
    except Exception as e:
        raise SensorException(e, sys)

if __name__ == '__main__':
    try:
        print("Dockerized")
    except Exception as e:
        logging.info(f"error: {e}")
        print(e)
