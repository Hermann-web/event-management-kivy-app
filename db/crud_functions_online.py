import os
import json
from setup import get_database
from utils import parse_mongo_obj_to_json_serializable
from config.config import COLLECTION_CLIENTS, COLLECTION_CLIENT_CHOICES, COLLECTION_EVENTS
from config.config import CLIENTS_TEMP_PATH, EVENTS_TEMP_PATH
from config.config import logging
from db.utils import get_present_time

def fetch_data_online(collection_name, filters):
    _, db = get_database()
    if filters:
        rows = db[collection_name].find(filters)
    else:
        rows = db[collection_name].find()
    return list(rows)

def save_to_temp(collection_name, rows, temp_path):
    # save temp
    rows = parse_mongo_obj_to_json_serializable(rows)
    # try to save to temp
    try:
        with open(temp_path, "w") as f: json.dump(rows, f)
        logging.info(f"...clients data save to {temp_path}")
    except Exception as e:
        logging.error(f"error when trying to save in temp, collection {collection_name}. e:{e}")
    
@catch_exceptions
def fetch_all_data(collection_name, temp_path=None, filters=None):
    """
    Retrieves a list of  documents from the  collection in the database.

    Returns:
    - List of documents.
    """
    if filters:
        filters = {key:val for key,val in filters.items() if val}
    if not filters:
        filters = None
    if not temp_path:
        logging.info(f"temp path will not be set for collection {collection_name}")
        return fetch_data_online(collection_name, filters)
    
    # create temp folder is not exist
    tmp_dir = os.path.normpath(os.path.join(temp_path,".."))
    
    if not os.path.exists(tmp_dir):
        logging.critical(f"temp_path {temp_path}: his folder does not exists. If It is a static table, it is better to save in temp in storage is not a problem")
        try:
            os.makedirs(tmp_dir)
            logging.info("folder created")
        except Exception as e:
            logging.error(f"could not create folder {tmp_dir}. error:{e}")
            return []
    
    # if the temp file not exists, fetch online
    if not os.path.exists(temp_path):
        # fetch online
        logging.info(f"temp_path {temp_path} not found. fetching online collection {collection_name}")
        rows = fetch_data_online(collection_name, filters=None)
        save_to_temp(collection_name, rows, temp_path)

    # it exists. so try to read it or fetch online
    try:
        with open(temp_path) as f: 
            rows = json.load(f)   
    except Exception as e:
        logging.warning(e)
        logging.info(f"temp_path {temp_path} not found. fetching online collection {collection_name}")
        rows = fetch_data_online(collection_name, filters=None)
        save_to_temp(collection_name, rows, temp_path)

    # apply filter
    if filters:
        rows = filter(lambda row:all([row[key]==filters[key] for key in filters]), rows)
    
    return list(rows)




def get_clients(filters=None):
    """
    Retrieves a list of client documents from the clients collection in the database.

    Returns:
    - List of client documents.
    """
    return list(fetch_all_data(collection_name=COLLECTION_CLIENTS, temp_path=CLIENTS_TEMP_PATH, filters=filters))

def get_events(filters=None):
    """
    Retrieves a list of event documents from the clients collection in the database.

    Returns:
    - List of event documents.
    """
    return list(fetch_all_data(collection_name=COLLECTION_EVENTS, temp_path=EVENTS_TEMP_PATH, filters=filters))

def get_client_choices(filters=None):
    """
    Retrieves a list of client_choice documents from the client_choices collection in the database.

    Returns:
    - List of client_choice documents.
    """
    return list(fetch_all_data(collection_name=COLLECTION_CLIENT_CHOICES, temp_path=None, filters=filters))



@catch_exceptions
def set_present_true(index):
    """
    Sets the 'is_present' field of a client_choice document to True if it is not already set.

    Parameters:
    - index (int): Index of the client_choice to modify.

    Returns:
    - The modified client_choice document.
    """
    _, db = get_database()
    choice = db[COLLECTION_CLIENT_CHOICES].find_one({'index': index})
    if not choice['is_present']:
        choice['is_present'] = True
        choice['time_presence'] = get_present_time()['time_presence']
        logging.info(f"set present = True for index = {index}")
        db[COLLECTION_CLIENT_CHOICES].replace_one({'index': index}, choice)
    return choice
