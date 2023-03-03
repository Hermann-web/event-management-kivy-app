import re
import pandas as pd
from pymongo import errors
from db.get_db import get_database


excel_file_path = "db/input/clients_example.xlsx"
sheet_name = "program"

def get_program_collection():
   # Get the database using the method we defined in pymongo_test_insert file
   dbname = get_database()
   collection = dbname["program"]
   return collection


def sanitize_client_data(df:pd.DataFrame):
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

def get_raw_programs():
      df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
      columns = ["time", "type", "lecturer", "day"]
      temp = set(columns) - set(df.columns)
      assert len(temp)==0, f"{temp} missing in program"
      sanitize_client_data(df)
      return df[columns].to_dict('records')

def client_insertion(collection, items:list):
      try:
         collection.insert_many(items)
         print("Client data inserted successfully.")
      except errors.BulkWriteError as e:
         for key,val in e.details['writeErrors'][0]['keyValue'].items():
            print(f"--> Error\n inserting client data: Duplicate key value {val} found for fields {key}.")

def load_program():
      collection = get_program_collection()
      items = get_raw_programs()
      print(f"--> Data:Items\n{items}")
      client_insertion(collection, items)
