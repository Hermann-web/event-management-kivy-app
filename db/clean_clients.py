import re
import pandas as pd
from setup import get_database, errors
from config import JSON_CLIENTS, RAW_JSON_CLIENTS
from config import RAW_JSON_EVENTS, JSON_EVENTS
from config import RAW_JSON_CLIENT_CHOICES, JSON_CLIENT_CHOICES
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
                                    cleaned_json_path, collection, **kwargs):
      df = get_raw_clients(json_fpath=raw_json_path,columns=columns)
      sanitize_fct(df,**kwargs)
      #items = df.to_dict('records')
      #print(f"--> Data:Items\n{items}")
      #client_insertion(collection, items)
      df.to_json(cleaned_json_path, orient="records", indent=4)


def get_client_collection(collection_name):
   # Get the database using the method we defined in pymongo_test_insert file
   _, dbname = get_database()
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


def get_event_collection(collection_name):
   # Get the database using the method we defined in pymongo_test_insert file
   _, dbname = get_database()
   collection = dbname[COLLECTION_EVENTS]
   try:
      collection.create_index("index", unique=True)
      print("--> Success\nUnique number index created successfully.")
   except errors.DuplicateKeyError:
      print("--> DoneAlready\nindex field already has unique constraint.")
   # pas de repetiton (day, hour)
   return collection

def get_user_event_collection(collection_name):
   # Get the database using the method we defined in pymongo_test_insert file
   _, dbname = get_database()
   collection = dbname[COLLECTION_CLIENT_CHOICES]
   try:
      collection.create_index("index", unique=True)
      print("--> Success\nUnique number index created successfully.")
   except errors.DuplicateKeyError:
      print("--> DoneAlready\nindex field already has unique constraint.")
   # make sure these id exists right ?
   return collection

def sanitize_client_data(df:pd.DataFrame):
      # Define regex patterns for each column
      patterns = {
         'index': r'[^a-zA-Z0-9]',
         'firstname': r'[^\w\s]',
         'surname': r'[^\w\s]',
         'email': r'[^\w@.-]',
         'reference': r'[^\w\s-]',
         'firm': r'[^\w\s-]',
         'role': r'[^\w\s-]',
         'cin': r'[^a-zA-Z0-9]'
      }

      # Check that "day" column only contains integers between 1 and 5
      assert df["index"].nunique() == len(df)

      # Apply regex patterns to each column of the DataFrame
      print(f"---------{df.columns}")
      for col, pattern in patterns.items():
         print(col, col in df.columns, df.columns)
         df[col] = df[col].apply(lambda x: re.sub(pattern, '', str(x).title()))

      # Convert email addresses to lowercase
      df['email'] = df['email'].apply(lambda x: x.lower())
      df['cin'] = df['cin'].apply(lambda x: x.upper())
      # Replace empty strings with None for firstname, surname, and email columns
      for col in ['firstname', 'surname', 'email']:
         df[col] = df[col].apply(lambda x: None if x == '' else x)
         assert df[col].isna().sum()==0


def sanitize_event_data(df:pd.DataFrame, **kwargs):
      format = kwargs["time_format"] or "%Hh%M"
      day_map = kwargs["day_map"]
      # Define regex patterns for each column
      patterns = {
         'index': r'[^a-zA-Z0-9]',
         'type': r'[^\w\s]',
         'lecturer': r'[^\w\s]'
      }

      # Check that "day" column only contains integers between 1 and 5
      assert df["index"].nunique() == len(df)

      # Apply regex patterns to each column of the DataFrame
      for col, pattern in patterns.items():
         df[col] = df[col].apply(lambda x: re.sub(pattern, '', str(x).title()))

      # Convert "time" column to a time object
      df["time"] = pd.to_datetime(df["time"], format=format).dt.time
      df["time"] = df["time"].apply(lambda t: t.strftime("%H:%M:%S"))

      # Convert "day" column to an integer
      if day_map is not None:
         # day_map = {"lundi": 1, "mardi": 2, "mercredi": 3, "jeudi": 4, "vendredi": 5}
         df["day"] = df["day"].apply(lambda x: day_map[x])
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

def sanitize_user_event_data(df:pd.DataFrame, **kwargs):
      format = kwargs["time_format"] or "%Hh%M"
      # Define regex patterns for each column
      patterns = {
         'index': r'[^a-zA-Z0-9]',
         'id_client': r'[^\w\s]',
         'id_event': r'[^\w\s]'
      }

      # Apply regex patterns to each column of the DataFrame
      for col, pattern in patterns.items():
         df[col] = df[col].apply(lambda x: re.sub(pattern, '', str(x).title()))

      # Check that "index" column is unique
      assert df["index"].nunique() == len(df)

      df.loc[df["is_present"].isna(),"is_present"] = False
      assert set(df["is_present"].unique()) == {True, False}

      # Convert "time_presence" column to a time object
      df["time_presence"] = pd.to_datetime(df["time_presence"], format=format).dt.time
      bool_idx = df["time_presence"].notna()
      df.loc[bool_idx,"time_presence"] = df.loc[bool_idx,"time_presence"].apply(lambda t: t.strftime("%H:%M:%S"))

      for col in set(df.columns)-{"time_presence"}:
         assert df[col].isna().sum()==0


def clean_clients():
      collection_name = COLLECTION_CLIENTS
      columns = ["index","firstname","surname","reference","firm","role","cin","email"]
      raw_json_path = RAW_JSON_CLIENTS
      cleaned_json_path = JSON_CLIENTS
      sanitize_fct=sanitize_client_data
      collection = get_user_event_collection(collection_name)
      preprocess_json_for_colllection(sanitize_fct=sanitize_fct, columns=columns, 
                                       raw_json_path=raw_json_path, cleaned_json_path=cleaned_json_path, 
                                       collection=collection)


def clean_events():
      collection_name = COLLECTION_EVENTS
      columns = ["index", "type", "lecturer", "day","time"]
      raw_json_path = RAW_JSON_EVENTS
      cleaned_json_path = JSON_EVENTS
      sanitize_fct=sanitize_event_data
      time_format = "%I:%M %p" #like "3:15 PM"
      day_map = {"2022-01-01":1, "2022-01-02":2, "2022-01-03":3, "2022-01-04":4 }
      collection = get_user_event_collection(collection_name)
      preprocess_json_for_colllection(sanitize_fct=sanitize_fct, columns=columns, 
                                       raw_json_path=raw_json_path, cleaned_json_path=cleaned_json_path, 
                                       collection=collection, time_format=time_format, day_map=day_map)

def clean_user_events():
      collection_name = COLLECTION_CLIENT_CHOICES
      columns = ["index","id_client", "id_event", "is_present", "time_presence"]
      raw_json_path = RAW_JSON_CLIENT_CHOICES
      cleaned_json_path = JSON_CLIENT_CHOICES
      sanitize_fct=sanitize_user_event_data
      time_format = "%I:%M %p" #like "3:15 PM"
      collection = get_user_event_collection(collection_name)
      preprocess_json_for_colllection(sanitize_fct=sanitize_fct, columns=columns, 
                                       raw_json_path=raw_json_path, cleaned_json_path=cleaned_json_path, 
                                       collection=collection, time_format=time_format)

