#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Hermann Agossou"

from config.config import PROD_ENV, logging


def setup():
    from backend.preprocess_json_for_colllection import clean_clients, clean_events, clean_user_events
    from backend.mongo_backup_and_load import import_json_data_to_mongodb_atlas

    logging.info("setup: ....clean_clients starting")
    clean_clients()
    logging.info("setup: ....clean_clients ended")

    logging.info("setup: ....clean_events starting")
    clean_events()
    logging.info("setup: ....clean_events ended")

    logging.info("setup: ....clean_user_events starting")
    clean_user_events()
    logging.info("setup: ....clean_user_events ended")

    logging.info("setup: ....send_data_online starting")
    if not PROD_ENV:
        import_json_data_to_mongodb_atlas()
        logging.info("setup: ....send_data_online ended")
    else:
        logging.info("setup: ... not doing this !!!")


if __name__ == "__main__":
    setup()
