#!/usr/bin/python3
"""This module defines a class to manage file storage for the HBNB clone"""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """This class manages storage of HBNB models in JSON format"""

    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is None:
            return self.__objects
        else:
            filtered_obj = {}
            for key, value in self.__objects.items():
                if isinstance(value, cls):
                    filtered_obj[key] = value
            return filtered_obj

    def new(self, obj):
        """Adds a new object to the storage dictionary"""
        key = obj.__class__.__name__ + '.' + obj.id
        self.__objects[key] = obj

    def delete(self, obj=None):
        """Deletes an object from the objects"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            if key in self.__objects:
                del self.__objects[key]
                self.save()

    def save(self):
        """Saves the storage dictionary to a file"""
        temp = {}
        for key, val in self.__objects.items():
            temp[key] = val.to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(temp, f)

    def reload(self):
        """Loads the storage dictionary from a file"""
        try:
            with open(self.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    cls_name = val['__class__']
                    cls = eval(cls_name)
                    self.__objects[key] = cls(**val)
        except FileNotFoundError:
            pass

    def close(self):
        """Deserializes the JSON file to objects"""
        self.reload()
