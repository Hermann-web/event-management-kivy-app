import json
from datetime import datetime
from config import get_database
from config import PROD_ENV
from config import JSON_CLIENTS,JSON_EVENTS,JSON_CLIENT_CHOICES
# colections names
from config import COLLECTION_CLIENTS,COLLECTION_EVENTS,COLLECTION_CLIENT_CHOICES

def create_backups(db):
    # Define the paths to the backup files
    BACKUP_CLIENTS = "db/backups/clients_backup_{}.json".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    BACKUP_EVENTS = "db/backups/events_backup_{}.json".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    BACKUP_CLIENT_CHOICES = "db/backups/client_choices_backup_{}.json".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    def parse_to_json_serializable(list_obj):
        list_obj = list(list_obj)
        for c in list_obj:
            c['_id'] = str(c['_id'])
        return list_obj

    with open(BACKUP_CLIENTS, 'w') as f:
        json.dump(parse_to_json_serializable(db[COLLECTION_CLIENTS].find()), f)
    with open(BACKUP_EVENTS, 'w') as f:
        json.dump(parse_to_json_serializable(db[COLLECTION_EVENTS].find()), f)
    with open(BACKUP_CLIENT_CHOICES, 'w') as f:
        json.dump(parse_to_json_serializable(db[COLLECTION_CLIENT_CHOICES].find()), f)

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
    if not PROD_ENV and 0:
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
