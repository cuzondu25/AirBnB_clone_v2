#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
import re

class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls == None:
            return FileStorage.__objects
        else:
            """Returns a dictionary of a specific class model in"""
            cls_dict = {}
            for key in FileStorage.__objects.keys():
                if re.match(cls.__name__, key):
                    cls_dict[key] = FileStorage.__objects[key]
            return cls_dict

    def get(self, cls, id):
        """A method to retrieve one object based on the object id"""
        import re
        self.reload()
        cls_obj = self.all(cls)

        id_obj = [obj for key, obj in cls_obj.items() if re.search(id, key)]
        if id_obj:
            return id_obj[0]
        else:
            return None

    def count(self, cls=None):
        """method to count the number of objects in storage"""
        #self.reload()
        if cls == None:
            cls_obj = self.all()
            return len(cls_obj)
        else:
            cls_obj = self.all(cls)
            return len(cls_obj)

    def delete(self, obj=None):
        """ to delete obj from __objects if it’s inside """
        if obj:
            for key in FileStorage.__objects.keys():
                if FileStorage.__objects[key] == obj:
                    del FileStorage.__objects[key]
                    break
            self.save()

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                        self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def close(self):
        self.reload()
