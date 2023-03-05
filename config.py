import os 
import logging

PROD_ENV = False
DEBUG = True
ONLINE = False

screen_login_str = 'login_screen'
screen_list_participants_str = 'list_screen'
screen_list_user_events_str = 'list_user_events_screen'
screen_list_events_str = 'list_events_screen'

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

BACKUP_FOLDER = "db/backups"
if not os.path.exists("db"):os.makedirs("db")
if not os.path.exists(BACKUP_FOLDER):os.makedirs(BACKUP_FOLDER)

COLLECTION_CLIENTS = "clients"
COLLECTION_EVENTS = "events"
COLLECTION_CLIENT_CHOICES = "client_choices"

TEMP_FOLDER = "tmp"
if not os.path.exists(TEMP_FOLDER):os.makedirs(TEMP_FOLDER)
CLIENTS_TEMP_PATH = "tmp/clients_tmp.json"



LOG_FOLDER = "logs"
if not os.path.exists(LOG_FOLDER):os.makedirs(LOG_FOLDER)

# Configure the logging module
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    handlers=[logging.FileHandler(f'{LOG_FOLDER}/myapp.log')])

# Example usage
# logging.debug('Debug message')
# logging.info('Info message')
# logging.warning('Warning message')
# logging.error('Error message')
# logging.critical('Critical message')