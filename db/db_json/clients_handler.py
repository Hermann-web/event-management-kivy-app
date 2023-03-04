import json

JSON_CLIENTS = "db_json\clients.json"
JSON_EVENTS = "db_json\events.json"
JSON_CLIENT_CHOICES = "db_json\client_choices.json"

def get_clients():
    """
    Reads the clients.json file and returns a list of client dictionaries.

    Returns:
    - List of client dictionaries.
    """
    with open(JSON_CLIENTS, 'r') as f:
        clients = json.load(f)
    return clients



def filter_clients(user_input):
    """
    Filters a list of client dictionaries based on a user input string.
    Filters by the client's firstname, surname, reference, or email fields.

    Parameters:
    - user_input (str): String to use for filtering.

    Returns:
    - List of filtered client dictionaries.
    """
    clients= get_clients()
    filtered_clients = []
    for client in clients:
        temp = ''.join(map(str,list(client.values()))).lower()
        if user_input.lower() in temp:
            filtered_clients.append(client)
        else:
            print(f"{user_input} not in {temp}")
    return filtered_clients


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

def filter_client_choices(id_client=None, id_event=None):
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
    if not id_client and not id_event:
        # If no filters are provided, return the full list
        return client_choices

    filtered_choices = []

    for choice in client_choices:
        if id_client and choice['id_client'] != id_client:
            continue
        if id_event and choice['id_event'] != id_event:
            continue
        filtered_choices.append(choice)

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
    
    