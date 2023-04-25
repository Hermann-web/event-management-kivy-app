# before everything especially (import kivy)
import os
import logging

## handle dir
KIVY_SYSTEM_FOLDER = os.path.abspath("./share")
os.environ["KIVY_HOME"] = KIVY_SYSTEM_FOLDER

## add timestamp
from kivy.logger import Logger, ColoredFormatter
# Set millisecond format to use a decimal because I'm in the US
logging.Formatter.default_msec_format = '%s.%03d'
# Add timestamp to log file
Logger.handlers[1].setFormatter(logging.Formatter('[%(asctime)s] %(message)s'))
# Add timestampt to console output
Logger.handlers[2].setFormatter(
    ColoredFormatter('[%(levelname)-18s] %(message)s'))
# ColoredFormatter('[%(levelname)-18s] [%(asctime)s] %(message)s'))
# logging.Formatter('[%(levelname)-5s] [%(asctime)s] %(message)s'))

logging = Logger
