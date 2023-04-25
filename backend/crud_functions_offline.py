import os
import json
from config.config import JSON_CLIENTS, JSON_EVENTS, JSON_CLIENT_CHOICES
from config.config import logging
from config.utils import log_exception, catch_exceptions
from backend.utils import get_present_time


def get_json_from_storage(json_file_path):
    with open(json_file_path, 'r') as f:
        rows = json.load(f)
    return rows


@catch_exceptions
def fetch_data_offline(json_file_path, filters=None):
    """
    Retrieves a list of  documents from the  collection in the database.

    Returns:
    - List of documents.
    """
    if filters:
        filters = {key: val for key, val in filters.items() if val}

    if not filters:
        filters = None

    if not os.path.exists(json_file_path):
        logging.critical(
            f"can't read data offline: the path does not exists {json_file_path}"
        )
        rows = []

    # fetch offline
    try:
        rows = get_json_from_storage(json_file_path=json_file_path)
    except Exception as e:
        logging.critical(
            f"can't read data offline from the path {json_file_path}")
        log_exception(e, "get_json_from_storage")
        rows = []

    # apply filter
    if filters:
        rows = filter(
            lambda row: all([row[key] == filters[key] for key in filters]),
            rows)

    return rows


def get_clients(filters=None):
    """
    Reads the clients.json file and returns a list of client dictionaries.

    Returns:
    - List of client dictionaries.
    """
    return fetch_data_offline(json_file_path=JSON_CLIENTS, filters=filters)


def get_events(filters=None):
    """
    Reads the clients.json file and returns a list of client dictionaries.

    Returns:
    - List of client dictionaries.
    """
    return fetch_data_offline(json_file_path=JSON_EVENTS, filters=filters)


def get_client_choices(filters=None):
    """
    Reads the client_choices.json file and returns a list of client_choice dictionaries.

    Returns:
    - List of client_choice dictionaries.
    """
    return fetch_data_offline(json_file_path=JSON_CLIENT_CHOICES,
                              filters=filters)


@catch_exceptions
def save_client_choices(client_choices):
    with open(JSON_CLIENT_CHOICES, 'w') as f:
        json.dump(client_choices, f, indent=4)


@catch_exceptions
def set_present_true(index):
    """
    Sets the 'is_present' value of a client_choice dictionary to True if it is not already set.

    Parameters:
    - client_choices (list of dict): List of client_choice dictionaries.
    - index (int): Index of the client_choice to modify.

    Returns:
    - The modified client_choice dictionary.
    """
    client_choices = get_client_choices()
    _ = [(row_number, row) for row_number, row in enumerate(client_choices)
         if row['index'] == index]
    row_number, choice = _[0]
    if not choice['is_present']:
        choice['is_present'] = True
        choice['time_presence'] = get_present_time()['time_presence']
        client_choices[row_number] = choice
        logging.info(f"set present = True for index = {choice['index']}")
        save_client_choices(client_choices)
    return choice
