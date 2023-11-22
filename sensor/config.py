from dataclasses import dataclass
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

MONGO_DB_URL_ENV_KEY = "MONGO_DB_URL"

@dataclass
class EnvironmentVariable:
    mongo_db_url:str = os.getenv(MONGO_DB_URL_ENV_KEY)


env_var = EnvironmentVariable()

mongo_client = MongoClient(env_var.mongo_db_url, server_api=ServerApi('1'))

