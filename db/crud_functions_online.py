import os
import json
from setup import get_database, parse_mongo_obj_to_json_serializable
from config import COLLECTION_CLIENTS, COLLECTION_CLIENT_CHOICES, COLLECTION_EVENTS
from config import CLIENTS_TEMP_PATH, EVENTS_TEMP_PATH
from config import logging

def get_clients():
    """
    Retrieves a list of client documents from the clients collection in the database.

    Returns:
    - List of client documents.
    """
    return fetch_all_data(COLLECTION_CLIENTS, CLIENTS_TEMP_PATH)

def get_events():
    """
    Retrieves a list of event documents from the clients collection in the database.

    Returns:
    - List of event documents.
    """
    return fetch_all_data(COLLECTION_EVENTS, EVENTS_TEMP_PATH)

def get_client_choices():
    """
    Retrieves a list of client_choice documents from the client_choices collection in the database.

    Returns:
    - List of client_choice documents.
    """
    _, db = get_database()
    client_choices = db[COLLECTION_CLIENT_CHOICES].find()
    return list(client_choices)


def fetch_all_data(collection_name, temp_path=None):
    """
    Retrieves a list of  documents from the  collection in the database.

    Returns:
    - List of documents.
    """
    if not temp_path:
        _, db = get_database()
        rows = db[collection_name].find()
        return rows
    
    if not os.path.exists(os.path.join(temp_path,"..")):
        logging.critical(f"temp_path {temp_path}: his folder does not exists")
        return []
    
    try:
        with open(temp_path) as f: 
            rows = json.load(f)
        return rows
    except Exception as e:
        logging.warning(e)
        _, db = get_database()
        clients = db[collection_name].find()
        clients = parse_mongo_obj_to_json_serializable(clients)
        # save to temp
        with open(temp_path, "w") as f: json.dump(clients, f)
        logging.info(f"...clients data save to {temp_path}")
        return clients

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
    if choice['is_present'] is None:
        choice['is_present'] = True
        db[COLLECTION_CLIENT_CHOICES].replace_one({'index': index}, choice)
    return choice
