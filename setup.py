#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__      = "Hermann Agossou"

from db.clean_clients import clean_clients, clean_events
from db.load_program import load_program
from db.mongoimport import import_json_data_to_mongodb_atlas

clean_clients()
clean_events()
#import_json_data_to_mongodb_atlas()