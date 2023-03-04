import re
import pandas as pd
from pymongo import errors
from db.get_db import get_database
from config import JSON_CLIENTS, RAW_JSON_CLIENTS
from config import RAW_JSON_EVENTS, JSON_EVENTS
from config import COLLECTION_CLIENTS, COLLECTION_EVENTS, COLLECTION_CLIENT_CHOICES


def get_raw_clients(json_fpath,columns):
      df = pd.read_json(json_fpath)
      temp = set(columns) - set(df.columns)
      assert len(temp)==0, f"{temp} missing in clients"
      return df[columns]

def client_insertion(collection, items:list):
      try:
         collection.insert_many(items)
         print("Client data inserted successfully.")
      except errors.BulkWriteError as e:
         for key,val in e.details['writeErrors'][0]['keyValue'].items():
            print(f"--> Error\n inserting client data: Duplicate key value {val} found for fields {key}.")

def preprocess_json_for_colllection(sanitize_fct, columns, raw_json_path, 
                                    cleaned_json_path, collection):
      df = get_raw_clients(json_fpath=raw_json_path,columns=columns)
      sanitize_client_data(df)
      #items = df.to_dict('records')
      #print(f"--> Data:Items\n{items}")
      #client_insertion(collection, items)
      df.to_json(cleaned_json_path, orient="records", indent=4)


def get_client_collection():
   # Get the database using the method we defined in pymongo_test_insert file
   dbname = get_database()
   collection = dbname[COLLECTION_CLIENTS]
   try:
      collection.create_index("index", unique=True)
      print("--> Success\nUnique number index created successfully.")
   except errors.DuplicateKeyError:
      print("--> DoneAlready\nindex field already has unique constraint.")
   try:
      collection.create_index("email", unique=True)
      print("--> Success\nUnique index email created successfully.")
   except errors.DuplicateKeyError:
      print("--> DoneAlready\nEmail field already has unique constraint.")
   try:
      collection.create_index([("cin", 1)], unique=True, sparse=True)
      print("--> Success\nUnique index cin created successfully.")
   except errors.DuplicateKeyError:
      print("--> DoneAlready\ncin field already has unique constraint.")
      
   return collection


def get_event_collection():
   # Get the database using the method we defined in pymongo_test_insert file
   dbname = get_database()
   collection = dbname[COLLECTION_EVENTS]
   try:
      collection.create_index("index", unique=True)
      print("--> Success\nUnique number index created successfully.")
   except errors.DuplicateKeyError:
      print("--> DoneAlready\nindex field already has unique constraint.")
   
   return collection


def sanitize_client_data(df:pd.DataFrame):
        # Define regex patterns for each column
        patterns = {
            'firstname': r'[^\w\s]',
            'surname': r'[^\w\s]',
            'email': r'[^\w@.-]',
            'reference': r'[^\w\s-]',
            'firm': r'[^\w\s-]',
            'role': r'[^\w\s-]',
            'cin': r'[^a-zA-Z0-9]'
        }

        # Apply regex patterns to each column of the DataFrame
        for col, pattern in patterns.items():
            df[col] = df[col].apply(lambda x: re.sub(pattern, '', str(x).title()))

        # Convert email addresses to lowercase
        df['email'] = df['email'].apply(lambda x: x.lower())
        df['cin'] = df['cin'].apply(lambda x: x.upper())
        # Replace empty strings with None for firstname, surname, and email columns
        for col in ['firstname', 'surname', 'email']:
            df[col] = df[col].apply(lambda x: None if x == '' else x)
            assert df[col].isna().sum()==0


def sanitize_event_data(df:pd.DataFrame):
        # Define regex patterns for each column
        patterns = {
            'type': r'[^\w\s]',
            'lecturer': r'[^\w\s]'
        }

        # Apply regex patterns to each column of the DataFrame
        for col, pattern in patterns.items():
            df[col] = df[col].apply(lambda x: re.sub(pattern, '', str(x).title()))
        
        # Convert "time" column to a time object
        df["time"] = pd.to_datetime(df["time"], format="%Hh%M").dt.time
        df["time"] = df["time"].apply(lambda t: t.strftime("%H:%M:%S"))
        
        # Convert "day" column to an integer
        # day_map = {"lundi": 1, "mardi": 2, "mercredi": 3, "jeudi": 4, "vendredi": 5}
        # df["day"] = df["day"].apply(lambda x: day_map[x])
        df["day"] = df["day"].astype("int")

        # Check that "day" column only contains integers between 1 and 5
        assert df["day"].isin(range(1, 6)).all()

        # tyoe
        df['type'] = df['type'].apply(lambda x: x.upper())
        assert df["type"].isin(['CONF',"ATLR","TUTO"]).all()

        # lecturer
        df['lecturer'] = df['lecturer'].apply(lambda x: x.title())

        # Replace empty strings with None for firstname, surname, and email columns
        for col in ["type", "lecturer"]:
            df[col] = df[col].apply(lambda x: None if x == '' else x)

        for col in df.columns:
            assert df[col].isna().sum()==0

def clean_clients():
      collection = get_client_collection()
      columns = ["index","firstname","surname","reference","firm","role","cin","email"]
      df = get_raw_clients(json_fpath=RAW_JSON_CLIENTS,columns=columns)
      sanitize_client_data(df)
      items = df.to_dict('records')
      print(f"--> Data:Items\n{items}")
      #client_insertion(collection, items)
      df.to_json(JSON_CLIENTS, orient="records", indent=4)



def clean_clients():
      columns = ["index","firstname","surname","reference","firm","role","cin","email"]
      collection = get_client_collection()
      raw_json_path = RAW_JSON_CLIENTS
      cleaned_json_path = JSON_CLIENTS
      sanitize_fct=sanitize_client_data
      preprocess_json_for_colllection(sanitize_fct=sanitize_fct, columns=columns, 
                                       raw_json_path=raw_json_path, cleaned_json_path=cleaned_json_path, 
                                       collection=collection)


def clean_events():
      columns = ["index","time", "type", "lecturer", "day"]
      collection = get_event_collection()
      raw_json_path = RAW_JSON_EVENTS
      cleaned_json_path = JSON_EVENTS
      sanitize_fct=sanitize_event_data
      preprocess_json_for_colllection(sanitize_fct=sanitize_fct, columns=columns, 
                                       raw_json_path=raw_json_path, cleaned_json_path=cleaned_json_path, 
                                       collection=collection)

