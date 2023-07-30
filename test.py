from sensor.utils import dump_csv_to_mongodb



if __name__ == '__main__':
    file_path = "E:/sensor_fault_detection/aps_failure_training_set1.csv"
    database_name = "sensor"
    collection_name = "sensor_readings"

    dump_csv_to_mongodb(file_path, database_name, collection_name)
