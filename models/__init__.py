#!/usr/bin/python3
"""
    Switch storage type directly by using the environment variable
    variable HBNB_TYPE_STORAGE.
"""
from os import getenv


if getenv("HBNB_TYPE_STORAGE") == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
