#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__      = "Hermann Agossou"

from pymongo import MongoClient, errors #do not remove (errors is used elsewhere)
from config import PROD_ENV
from config import CONNECTION_STRING, DATABASE_NAME


def get_database():
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
    print(f"....send_data_online ended")

if __name__ =="__main__":
    setup()