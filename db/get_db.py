#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__      = "Hermann Agossou"

# source
# https://www.mongodb.com/languages/python#prerequisites
# 
from pymongo import MongoClient
from dateutil import parser

def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb+srv://pkaCbXZuJtChwHlaMcbr:Uz51Mew4Y0NmQP0C@cluster0.x4jt5zg.mongodb.net/?retryWrites=true&w=majority"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['AttendanceDb']

'''def get_items(items):
   expiry_date = '2021-07-13T00:00:00.000Z'
   expiry = parser.parse(expiry_date)
   items = [{
      "item_name" : "Bread",
      "quantity" : 2,
      "ingredients" : "all-purpose flour",
      "expiry_date" : expiry
   }]
   return items



def get_item_collection():
   # Get the database using the method we defined in pymongo_test_insert file
   dbname = get_database()
   collection_name = dbname["attendance"]
   return collection_name

def insert(item):
   collection_name = get_collection()
   item = get_items([item])[0]
   collection_name.insert_one(item)

def insert_many(items):
   collection_name = get_collection()
   items = get_items(items)
   collection_name.insert_many(items)

def get_data(selection=None):
   collection_name = get_collection()
   if selection is None:
      res = collection_name.find()
   else:
      assert isinstance(selection, dict)
      res = collection_name.find(selection)
'''