from config import ONLINE 
from config import logging

if ONLINE:
    logging.info("ONLINE = {ONLINE}. working with online db")
    from db.crud_functions_online import (
        get_clients, filter_clients, get_client_choices, 
        filter_client_choices, filter_client_choices_from_text_input,
        set_present_true
        )
else:
    logging.info("ONLINE = {ONLINE}. working with local db")
    from db.db_json.clients_handler import (
        get_clients, filter_clients, get_client_choices, 
        filter_client_choices, filter_client_choices_from_text_input,
        set_present_true
        )
