import pandas as pd
import logging
import json
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
        raise e


