from pymongo import MongoClient

def connect_to_database():
    """
    Connects to the MongoDB Atlas database and returns a MongoClient object.

    Returns:
    - MongoClient object.
    """
    # Replace the placeholders with your MongoDB Atlas connection string and database name
    # You can get the connection string from your Atlas dashboard
    conn_str = 'mongodb+srv://pkaCbXZuJtChwHlaMcbr:Uz51Mew4Y0NmQP0C@cluster0.x4jt5zg.mongodb.net/?retryWrites=true&w=majority'
    db_name = 'AttendanceDb'
    
    client = MongoClient(conn_str)
    db = client[db_name]
    
    return db


def get_clients():
    """
    Retrieves a list of client documents from the clients collection in the database.

    Returns:
    - List of client documents.
    """
    db = connect_to_database()
    clients = db.clients.find()
    return list(clients)


def filter_clients(user_input):
    """
    Filters client documents in the clients collection based on a user input string.
    Filters by the client's firstname, surname, reference, or email fields.

    Parameters:
    - user_input (str): String to use for filtering.

    Returns:
    - List of filtered client documents.
    """
    db = connect_to_database()
    filter_query = {
        '$or': [
            {'firstname': {'$regex': user_input, '$options': 'i'}},
            {'surname': {'$regex': user_input, '$options': 'i'}},
            {'reference': {'$regex': user_input, '$options': 'i'}},
            {'email': {'$regex': user_input, '$options': 'i'}}
        ]
    }
    filtered_clients = db.clients.find(filter_query)
    return list(filtered_clients)


def get_client_choices():
    """
    Retrieves a list of client_choice documents from the client_choices collection in the database.

    Returns:
    - List of client_choice documents.
    """
    db = connect_to_database()
    client_choices = db.client_choices.find()
    return list(client_choices)


def filter_client_choices(id_client=None, id_event=None):
    """
    Filters client_choice documents in the client_choices collection based on the provided id_client and/or id_event.
    If neither id_client nor id_event are provided, returns the full list.

    Parameters:
    - id_client (int, optional): ID of the client to filter by.
    - id_event (int, optional): ID of the event to filter by.

    Returns:
    - List of filtered client_choice documents.
    """
    db = connect_to_database()
    filter_query = {}
    if id_client:
        filter_query['id_client'] = id_client
    if id_event:
        filter_query['id_event'] = id_event
    if not filter_query:
        # If no filters are provided, return the full list
        filtered_choices = db.client_choices.find()
    else:
        filtered_choices = db.client_choices.find(filter_query)
    return list(filtered_choices)


def set_present_true(index):
    """
    Sets the 'is_present' field of a client_choice document to True if it is not already set.

    Parameters:
    - index (int): Index of the client_choice to modify.

    Returns:
    - The modified client_choice document.
    """
    db = connect_to_database()
    choice = db.client_choices.find_one({'index': index})
    if choice['is_present'] is None:
        choice['is_present'] = True
        db.client_choices.replace_one({'index': index}, choice)
    return choice
