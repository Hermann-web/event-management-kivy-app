import os
import json
from setup import get_database, parse_mongo_obj_to_json_serializable
from config import COLLECTION_CLIENTS, COLLECTION_CLIENT_CHOICES
from config import CLIENTS_TEMP_PATH



def get_clients():
    """
    Retrieves a list of client documents from the clients collection in the database.

    Returns:
    - List of client documents.
    """
    try:
        with open(CLIENTS_TEMP_PATH) as f: 
            clients = json.load(f)
    except Exception as e:
        print("warning:",e)
        _, db = get_database()
        clients = db[COLLECTION_CLIENTS].find()
        clients = parse_mongo_obj_to_json_serializable(clients)
        # save to temp
        with open(CLIENTS_TEMP_PATH, "w") as f: json.dump(clients, f)
        print(f"...clients data save to ",CLIENTS_TEMP_PATH)
    return clients


def filter_clients(user_input):
    """
    Filters client documents in the clients collection based on a user input string.
    Filters by the client's firstname, surname, reference, or email fields.

    Parameters:
    - user_input (str): String to use for filtering.

    Returns:
    - List of filtered client documents.
    """
    _, db = get_database()
    filter_query = {
        '$or': [
            {'firstname': {'$regex': user_input, '$options': 'i'}},
            {'surname': {'$regex': user_input, '$options': 'i'}},
            {'reference': {'$regex': user_input, '$options': 'i'}},
            {'email': {'$regex': user_input, '$options': 'i'}}
        ]
    }
    filtered_clients = db[COLLECTION_CLIENTS].find(filter_query)
    return list(filtered_clients)


def get_client_choices():
    """
    Retrieves a list of client_choice documents from the client_choices collection in the database.

    Returns:
    - List of client_choice documents.
    """
    _, db = get_database()
    client_choices = db[COLLECTION_CLIENT_CHOICES].find()
    return list(client_choices)


def filter_client_choices(id_client=None, id_event=None, day=None, hour=None):
    """
    Filters client_choice documents in the client_choices collection based on the provided id_client and/or id_event.
    If neither id_client nor id_event are provided, returns the full list.

    Parameters:
    - id_client (int, optional): ID of the client to filter by.
    - id_event (int, optional): ID of the event to filter by.

    Returns:
    - List of filtered client_choice documents.
    """
    _, db = get_database()
    filter_query = {}
    if id_client:
        filter_query['id_client'] = id_client
    if id_event:
        filter_query['id_event'] = id_event
    if day:
        filter_query['day'] = day
    if hour:
        filter_query['hour'] = hour
    if not filter_query:
        # If no filters are provided, return the full list
        filtered_choices = db[COLLECTION_CLIENT_CHOICES].find()
    else:
        filtered_choices = db[COLLECTION_CLIENT_CHOICES].find(filter_query)
    return list(filtered_choices)


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
