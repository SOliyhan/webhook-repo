from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

def db_connection():
    connection_string = os.environ.get("CONNECTION_STRING")
    client = MongoClient(connection_string)
    dbs = client.list_database_names()
    
    webhookDb = client.webhookDb
    collection = webhookDb.webhook

    return collection



