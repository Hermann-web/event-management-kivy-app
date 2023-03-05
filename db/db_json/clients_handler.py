import json
from config import JSON_CLIENTS, JSON_EVENTS, JSON_CLIENT_CHOICES

def get_clients():
    """
    Reads the clients.json file and returns a list of client dictionaries.

    Returns:
    - List of client dictionaries.
    """
    with open(JSON_CLIENTS, 'r') as f:
        clients = json.load(f)
    return clients

def get_events():
    """
    Reads the clients.json file and returns a list of client dictionaries.

    Returns:
    - List of client dictionaries.
    """
    with open(JSON_EVENTS, 'r') as f:
        events = json.load(f)
    return events

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
    
    