PROD_ENV = True

screen_login_str = 'login_screen'
screen_list_participants_str = 'list_screen'
screen_list_user_events_str = 'list_user_events_screen'

# Provide the mongodb atlas url to connect python to mongodb using pymongo
CONNECTION_STRING = "mongodb+srv://pkaCbXZuJtChwHlaMcbr:Uz51Mew4Y0NmQP0C@cluster0.x4jt5zg.mongodb.net/?retryWrites=true&w=majority"
DATABASE_NAME = "AttendanceDb" if PROD_ENV else "AttendanceDbTest"



# Define the paths to the JSON data files
JSON_CLIENTS = "db/db_json/clients_clean.json"
RAW_JSON_CLIENTS = "db/db_json/clients_raw.json"
JSON_EVENTS = "db/db_json/events_clean.json"
RAW_JSON_EVENTS = "db/db_json/events_raw.json"
JSON_CLIENT_CHOICES = "db/db_json/client_choices_clean.json"
RAW_JSON_CLIENT_CHOICES = "db/db_json/client_choices_raw.json"


COLLECTION_CLIENTS = "clients"
COLLECTION_EVENTS = "events"
COLLECTION_CLIENT_CHOICES = "client_choices"
