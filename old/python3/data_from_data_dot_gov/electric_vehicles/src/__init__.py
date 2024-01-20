#!/usr/bin/python3
"""Creates an instance of the database and makes a call to the
create_all function
"""

from src.engine.db_engine import DbEngine

db_storage = DbEngine()
db_storage.create_all()
