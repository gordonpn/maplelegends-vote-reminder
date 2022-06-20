"""Singleton module
"""
import logging
import os
from threading import Lock
from typing import Any

from pymongo import MongoClient
from pymongo.database import Database


class SingletonMeta(type):
    """
    This is a thread-safe implementation of Singleton.
    """

    _instances: dict[Any, Any] = {}

    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class DB(metaclass=SingletonMeta):
    """
    Database singleton class
    """

    def __init__(self) -> None:
        self.log = logging.getLogger("discord_bot")
        db_host = os.getenv("MONGO_HOST")
        db_username = os.getenv("MONGO_NON_ROOT_USERNAME")
        db_password = os.getenv("MONGO_NON_ROOT_PASSWORD")
        db_name = os.getenv("MONGO_INITDB_DATABASE")
        if not db_name:
            raise ValueError("Database string should not be empty")
        uri: str = f"mongodb://{db_username}:{db_password}@{db_host}:27017/{db_name}"
        self.log.debug("Connection string: %s", uri)
        connection: MongoClient = MongoClient(uri, fsync=True)
        self.database: Database = connection[db_name]
        self.log.info("Database initialized")

    def get_timestamp_collection(self):
        """Returns the timestamp collection"""
        return self.database.collection["vote_timestamps"]

    def get_registered_users(self):
        """Returns the registered users collection"""
        return self.database.collection["registered_users"]
