#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__      = "Hermann Agossou"

# source
# https://www.mongodb.com/languages/python#prerequisites
# 
from setup import get_database
from dateutil import parser


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
   _, dbname = get_database()
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