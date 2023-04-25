import re
from unidecode import unidecode
from config.config import ONLINE
from config.config import logging
from config.utils import catch_exceptions

if ONLINE:
    logging.info(f"ONLINE: {ONLINE}. working with online db")
    from backend.crud_functions_online import (get_clients, get_events,
                                               get_client_choices,
                                               set_present_true)
else:
    logging.info(f"ONLINE: {ONLINE}. working with local db")
    from backend.crud_functions_offline import (get_clients, get_events,
                                                get_client_choices,
                                                set_present_true)


@catch_exceptions
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
    results = get_client_choices(filters={
        'id_client': id_client,
        'id_event': id_event,
        'day': day,
        'hour': hour
    })
    return list(results)


@catch_exceptions
def filter_json_from_text(json_data, text_input):
    """
    Filters documents in the json_data dictionary based on the provided text_input.
    If text_input is None, returns the full list.

    Parameters:
    - json_data (list[dict]): Dictionary containing documents.
    - text_input (str): Text input containing fields to filter by. Fields should be separated by spaces.

    Returns:
    - List of filtered documents.
    """

    keys = []

    if text_input:
        # Preprocess text input by removing diacritics and unwanted characters
        text_input = unidecode(text_input.lower())
        text_input = re.sub(r'[^\w\s]', '', text_input)
        text_input = re.sub(r'\s+', ' ', text_input)

        # Split text input into fields and construct filter query
        keys = [key.strip().lower() for key in text_input.split(' ')]
        #keys = list(filter(lambda x: len(x)>2, keys))

    if not keys:
        # If no filters are provided, return the full list
        filtered_choices = list(json_data)
    else:
        logging.debug(f"keys: {keys}")
        filter_ = [
            (j,
             sum([
                 int(key in "-".join(list(map(str, doc.values()))).lower())
                 for key in keys
             ])) for j, doc in enumerate(json_data)
        ]
        logging.debug(f"filter_: {filter_}")
        filtered_choices = [
            json_data[i] for i in map(
                lambda x: x[0],
                sorted(list(filter(lambda x: x[1] != 0, filter_)),
                       key=lambda x: x[1],
                       reverse=True))
        ]

    return list(filtered_choices)


@catch_exceptions
def filter_clients_from_text_input(text_input: str = None,
                                   filters: dict = None):
    """
    Filters client documents in the json_data dictionary based on the provided text_input.
    If text_input is None, returns the full list.

    Parameters:
    - json_data (list[dict]): Dictionary containing client documents.
    - text_input (str): Text input containing fields to filter by. Fields should be separated by spaces.

    Returns:
    - List of filtered client documents.
    """
    json_data = get_clients(filters=filters)
    results = filter_json_from_text(json_data,
                                    text_input) if text_input else json_data
    return list(results)


@catch_exceptions
def filter_event_from_text_input(text_input: str = None, filters: dict = None):
    """
    Filters client_choice documents in the json_data dictionary based on the provided text_input.
    If text_input is None, returns the full list.

    Parameters:
    - json_data (dict): Dictionary containing client_choice documents.
    - text_input (str): Text input containing fields to filter by. Fields should be separated by spaces.

    Returns:
    - List of filtered client_choice documents.
    """
    json_data = get_events(filters=filters)
    results = filter_json_from_text(json_data,
                                    text_input) if text_input else json_data
    return list(results)


@catch_exceptions
def filter_client_choices_from_text_input(text_input: str = None,
                                          filters: dict = None):
    """
    Filters client_choice documents in the json_data dictionary based on the provided text_input.
    If text_input is None, returns the full list.

    Parameters:
    - json_data (dict): Dictionary containing client_choice documents.
    - text_input (str): Text input containing fields to filter by. Fields should be separated by spaces.

    Returns:
    - List of filtered client_choice documents.
    """
    json_data = get_client_choices(filters=filters)
    results = filter_json_from_text(json_data,
                                    text_input) if text_input else json_data
    return list(results)
