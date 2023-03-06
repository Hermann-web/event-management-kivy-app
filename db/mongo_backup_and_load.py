import json
from datetime import datetime
from utils import parse_mongo_obj_to_json_serializable, get_database
from config import PROD_ENV
from config import JSON_CLIENTS,JSON_EVENTS,JSON_CLIENT_CHOICES
# colections names
from config import COLLECTION_CLIENTS,COLLECTION_EVENTS,COLLECTION_CLIENT_CHOICES


def create_backups(db):
    # Define the paths to the backup files
    test_or_prod = "prod" if PROD_ENV==True else "test"
    time_ = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    BACKUP_CLIENTS = f"db/backups/{test_or_prod}_clients_backup_{time_}.json"
    BACKUP_EVENTS = f"db/backups/{test_or_prod}_events_backup_{time_}.json"
    BACKUP_CLIENT_CHOICES = f"db/backups/{test_or_prod}_client_choices_backup_{time_}.json"

    with open(BACKUP_CLIENTS, 'w') as f:
        json.dump(parse_mongo_obj_to_json_serializable(db[COLLECTION_CLIENTS].find()), f)
    with open(BACKUP_EVENTS, 'w') as f:
        json.dump(parse_mongo_obj_to_json_serializable(db[COLLECTION_EVENTS].find()), f)
    with open(BACKUP_CLIENT_CHOICES, 'w') as f:
        json.dump(parse_mongo_obj_to_json_serializable(db[COLLECTION_CLIENT_CHOICES].find()), f)

def delete_collections(db):
    # Delete all documents from the clients, events, and client_choices collections
    db.clients.delete_many({})
    db.events.delete_many({})
    db.client_choices.delete_many({})


def import_local_json_online_bdd(db):
    # Load the clients JSON data and insert it into the clients collection
    with open(JSON_CLIENTS, 'r') as f:
        clients_data = json.load(f)
        db.clients.insert_many(clients_data)

    # Load the events JSON data and insert it into the events collection
    with open(JSON_EVENTS, 'r') as f:
        events_data = json.load(f)
        db.events.insert_many(events_data)

    # Load the client_choices JSON data and insert it into the client_choices collection
    with open(JSON_CLIENT_CHOICES, 'r') as f:
        client_choices_data = json.load(f)
        db.client_choices.insert_many(client_choices_data)




def import_json_data_to_mongodb_atlas():
    if not PROD_ENV:
        # Connect to the MongoDB Atlas cluster
        client, db = get_database()
        # Create backups of the clients, events, and client_choices collections
        create_backups(db)
        # Delete all documents from the clients, events, and client_choices collections
        delete_collections(db)
        # Load the all clollections JSON data and insert it into the db online
        import_local_json_online_bdd(db)
        # Close the MongoDB Atlas connection
        client.close()
    else:
        print(".... not doing shit !!!")