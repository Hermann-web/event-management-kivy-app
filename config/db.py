#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Hermann Agossou"

from pymongo import MongoClient, errors  #do not remove (errors is used elsewhere)
import sqlite3
from config.config import PROD_ENV, ONLINE
from config.config import CONNECTION_STRING, DATABASE_NAME
from config.config import SQLITE_DB
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
