#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__      = "Hermann Agossou"

from pymongo import MongoClient, errors #do not remove (errors is used elsewhere)
from config.config import PROD_ENV, ONLINE
from config.config import CONNECTION_STRING, DATABASE_NAME
from config.config import logging 

logging.info(f"...PROD_ENV: is set to {PROD_ENV}")
logging.info(f"...DATABASE_NAME: {DATABASE_NAME}")
logging.info(f"...ONLINE: is set to {ONLINE}")



def get_database():
    logging.info(f"database call: {DATABASE_NAME}")
    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)
    # Create the database for our example (we will use the same database throughout the tutorial
    return client, client[DATABASE_NAME]


def setup():
    from db.preprocess_json_for_colllection import clean_clients, clean_events, clean_user_events
    from db.mongo_backup_and_load import import_json_data_to_mongodb_atlas
    

    print(f"....clean_clients starting")
    clean_clients()
    print(f"....clean_clients ended")

    print(f"....clean_events starting")
    clean_events()
    print(f"....clean_events ended")

    print(f"....clean_user_events starting")
    clean_user_events()
    print(f"....clean_user_events ended")

    print(f"....send_data_online starting")
    if not PROD_ENV: import_json_data_to_mongodb_atlas()
    else: print("... not doing this !!!")
    print(f"....send_data_online ended")

if __name__ =="__main__":
    setup()