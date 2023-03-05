import json
from config import JSON_CLIENTS, JSON_EVENTS, JSON_CLIENT_CHOICES
import re
from unidecode import unidecode

def get_clients():
    """
    Reads the clients.json file and returns a list of client dictionaries.

    Returns:
    - List of client dictionaries.
    """
    with open(JSON_CLIENTS, 'r') as f:
        clients = json.load(f)
    return clients




def filter_clients(text_input):
    """
    Filters client documents in the json_data dictionary based on the provided text_input.
    If text_input is None, returns the full list.

    Parameters:
    - json_data (list[dict]): Dictionary containing client documents.
    - text_input (str): Text input containing fields to filter by. Fields should be separated by spaces.

    Returns:
    - List of filtered client documents.
    """
    json_data = get_clients()
    keys = []

    if text_input:
        # Preprocess text input by removing diacritics and unwanted characters
        text_input = unidecode(text_input.lower())
        text_input = re.sub(r'[^\w\s]', '', text_input)
        text_input = re.sub(r'\s+', ' ', text_input)

        # Split text input into fields and construct filter query
        keys = [key.strip().lower() for key in text_input.split(' ')]
        keys = list(filter(lambda x: len(x)>2, keys))


    if not keys:
        # If no filters are provided, return the full list
        filtered_choices = list(json_data)
    else:
        print(f"keys: {keys}")
        filter_ = [(j,sum([int(key in "-".join(list(map(str,doc.values()))).lower()) for key in keys])) for j,doc in enumerate(json_data) ]
        print("1",filter_)
        filtered_choices =  [json_data[i] for i in map(lambda x: x[0], sorted(filter(lambda x: x[1]!=0, filter_), key=lambda x:x[1], reverse=True))]

    return filtered_choices

def get_client_choices():
    """
    Reads the client_choices.json file and returns a list of client_choice dictionaries.

    Returns:
    - List of client_choice dictionaries.
    """
    with open(JSON_CLIENT_CHOICES, 'r') as f:
        client_choices = json.load(f)
    return client_choices

def save_client_choices(client_choices):
    with open(JSON_CLIENT_CHOICES, 'w') as f:
        json.dump(client_choices, f, indent=4)


def save_client_choices(client_choices):
    with open(JSON_CLIENT_CHOICES, 'w') as f:
        json.dump(client_choices, f, indent=4)

def filter_client_choices(id_client=None, id_event=None, day=None, hour=None):
    """
    Filters a list of client_choices dictionaries based on the provided id_client and/or id_event.
    If neither id_client nor id_event are provided, returns the full list.
    Parameters:
    - id_client (int, optional): ID of the client to filter by.
    - id_event (int, optional): ID of the event to filter by.
    Returns:
    - List of filtered client_choices dictionaries.
    """
    client_choices = get_client_choices()
    if not id_client and not id_event and not day and not hour:
        # If no filters are provided, return the full list
        return client_choices

    filtered_choices = []

    for choice in client_choices:
        if id_client and choice['id_client'] not in id_client:
            continue
        if id_event and choice['id_event'] not in id_event:
            continue
        if day and choice['day'] not in day:
            continue
        if hour and choice['hour'] not in hour:
            continue
        filtered_choices.append(choice)

    return filtered_choices

def filter_client_choices_from_text_input(text_input):
    """
    Filters client_choice documents in the json_data dictionary based on the provided text_input.
    If text_input is None, returns the full list.

    Parameters:
    - json_data (dict): Dictionary containing client_choice documents.
    - text_input (str): Text input containing fields to filter by. Fields should be separated by spaces.

    Returns:
    - List of filtered client_choice documents.
    """
    json_data = get_client_choices()
    filter_query = {}

    if text_input:
        # Preprocess text input by removing diacritics and unwanted characters
        text_input = unidecode(text_input.lower())
        text_input = re.sub(r'[^\w\s]', '', text_input)
        text_input = re.sub(r'\s+', ' ', text_input)

        # Split text input into fields and construct filter query
        fields = [field.strip() for field in text_input.split(' ')]
        for field in fields:
            filter_query[field] = {'$regex': f'.*{field}.*', '$options': 'i'}

    if not filter_query:
        # If no filters are provided, return the full list
        filtered_choices = list(json_data)
    else:
        # Filter client_choice documents that contain each field in the text_input
        filtered_choices = [doc for doc in json_data if all(re.search(filter_query[field]['$regex'], doc.get(field, ''), re.IGNORECASE) for field in filter_query)]

    return filtered_choices

def set_present_true(index, force_null_test=False):
    """
    Sets the 'is_present' value of a client_choice dictionary to True if it is not already set.

    Parameters:
    - client_choices (list of dict): List of client_choice dictionaries.
    - index (int): Index of the client_choice to modify.

    Returns:
    - The modified client_choice dictionary.
    """
    client_choices = get_client_choices()
    choice = client_choices[index-1]
    if choice['is_present'] is None:
        choice['is_present'] = True
        save_client_choices(client_choices)
        return choice
    elif force_null_test==True:
        choice['is_present'] = None
        save_client_choices(client_choices)
        return choice
    else:
        return choice
    
    