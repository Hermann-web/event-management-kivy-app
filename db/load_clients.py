import re
import pandas as pd
from pymongo import errors
from db.get_db import get_database


excel_file_path = "db/input/clients_example.xlsx"
sheet_name = "clients"

def get_client_collection():
   # Get the database using the method we defined in pymongo_test_insert file
   dbname = get_database()
   collection = dbname["client"]
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

def get_raw_clients():
      df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
      columns = ["firstname","surname","reference","firm","role","cin","email"]
      temp = set(columns) - set(df.columns)
      assert len(temp)==0, f"{temp} missing in clients"
      sanitize_client_data(df)
      return df[columns].to_dict('records')

def client_insertion(collection, items:list):
      try:
         collection.insert_many(items)
         print("Client data inserted successfully.")
      except errors.BulkWriteError as e:
         for key,val in e.details['writeErrors'][0]['keyValue'].items():
            print(f"--> Error\n inserting client data: Duplicate key value {val} found for fields {key}.")

def load_clients():
      collection = get_client_collection()
      items = get_raw_clients()
      print(f"--> Data:Items\n{items}")
      client_insertion(collection, items)
