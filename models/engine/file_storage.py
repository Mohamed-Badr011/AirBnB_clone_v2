#!/usr/bin/python3
"""
Contains the FileStorage class for managing data serialization and deserialization
between Python objects and a JSON file.

Classes:
    FileStorage: Handles storage of Python objects in JSON format and retrieval of objects.
"""

import json
import models
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from hashlib import md5

# A dictionary mapping class names to their corresponding class objects
classes = {
    "Amenity": Amenity,
    "BaseModel": BaseModel,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User
}


class FileStorage:
    """
    Serializes instances to a JSON file and deserializes JSON file back to instances.

    Attributes:
        __file_path (str): Path to the JSON file used for storage.
        __objects (dict): A dictionary storing all objects, keyed by "<class name>.id".
    """

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """
        Returns the dictionary of objects in storage. If a class is specified,
        only objects of that class are returned.

        Args:
            cls (class, optional): The class to filter objects by. Defaults to None.

        Returns:
            dict: A dictionary of objects filtered by class or all objects.
        """
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """
        Adds a new object to the storage dictionary.

        Args:
            obj (BaseModel): The object to be added to storage.
        """
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """
        Serializes the storage dictionary to the JSON file.
        """
        json_objects = {}
        for key in self.__objects:
            if key == "password":
                json_objects[key].decode()
            json_objects[key] = self.__objects[key].to_dict(save_fs=1)
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """
        Deserializes the JSON file back into the storage dictionary.
        If the file does not exist, the method does nothing.
        """
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except:
            pass

    def delete(self, obj=None):
        """
        Deletes an object from the storage dictionary, if it exists.

        Args:
            obj (BaseModel, optional): The object to be deleted. Defaults to None.
        """
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """
        Calls the reload() method to deserialize the JSON file into objects.
        """
        self.reload()

    def get(self, cls, id):
        """
        Retrieves an object based on its class and ID.

        Args:
            cls (class): The class of the object to retrieve.
            id (str): The ID of the object to retrieve.

        Returns:
            BaseModel: The retrieved object, or None if not found.
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

