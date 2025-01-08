#!/usr/bin/python3
"""
This module defines the DBStorage class, which provides an interface to interact
with a MySQL database using SQLAlchemy.

Classes:
    DBStorage: A class that manages interactions between the application and the
               MySQL database, supporting CRUD operations and advanced queries.
"""

import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# A dictionary mapping class names to their corresponding class objects
classes = {
    "Amenity": Amenity,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User
}


class DBStorage:
    """
    Interacts with the MySQL database using SQLAlchemy.

    Attributes:
        __engine (sqlalchemy.engine.Engine): The SQLAlchemy engine for database connections.
        __session (sqlalchemy.orm.scoped_session): The scoped session for managing database queries.
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes a DBStorage instance by creating a database engine and,
        if in test environment, dropping all existing tables.
        """
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Queries the current database session for all objects of a specific class,
        or all objects if no class is specified.

        Args:
            cls (class, optional): The class to filter objects by. Defaults to None.

        Returns:
            dict: A dictionary of objects, keyed by '<class name>.<object id>'.
        """
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """
        Adds the object to the current database session.

        Args:
            obj (BaseModel): The object to be added.
        """
        self.__session.add(obj)

    def save(self):
        """
        Commits all changes of the current database session.
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes the object from the current database session, if it exists.

        Args:
            obj (BaseModel, optional): The object to be deleted. Defaults to None.
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
        Reloads the database by creating all tables and initializing a new scoped session.
        """
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """
        Closes the session by calling the remove() method on the private session attribute.
        """
        self.__session.remove()

    def get(self, cls, id):
        """
        Retrieves an object based on its class and ID.

        Args:
            cls (class): The class of the object.
            id (str): The ID of the object.

        Returns:
            BaseModel: The object if found, otherwise None.
        """
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if value.id == id:
                return value
        return None

    def count(self, cls=None):
        """
        Counts the number of objects in storage, optionally filtered by class.

        Args:
            cls (class, optional): The class to filter objects by. Defaults to None.

        Returns:
            int: The number of objects in storage.
        """
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(models.storage.all(clas).values())
        else:
            count = len(models.storage.all(cls).values())

        return count

