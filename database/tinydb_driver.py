import os
import sys
import logging
from tinydb import TinyDB


tinydb: TinyDB = None


def tinydb_init():
    global tinydb

    if os.environ['ENV'] == 'dev':
        tdb_path = os.environ['TDB_DEV_PATH']
    elif os.environ['ENV'] == 'prod':
        tdb_path = os.environ['TDB_PATH']

    try:
        tinydb = TinyDB(tdb_path)
        logging.getLogger('uvicorn').info(f"Loaded database file: {tdb_path}")
    except Exception as e:
        logging.getLogger('uvicorn').error(f"Can not loaded database file: {tdb_path}, Error: {e}")
        sys.exit(1)


def get_database() -> TinyDB | None:
    return tinydb
