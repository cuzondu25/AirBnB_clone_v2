#!/usr/bin/python3
""" SQL storage engine"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base

class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """enviromental variables"""
        env = getenv("HBNB_ENV")                    #running environment. It can be “dev” or “test”
        username = getenv("HBNB_MYSQL_USER")        # the username of your MySQL
        password = getenv("HBNB_MYSQL_PWD")         # the password of your MySQL
        hostname = getenv("HBNB_MYSQL_HOST", default="localhost") # the hostname of your MySQL
        db_name = getenv("HBNB_MYSQL_DB")           # the database name of your MySQL
        # type of storage used. a “file” (using FileStorage) or db (using DBStorage)
        db_storage = getenv("HBNB_TYPE_STORAGE")    
        
        db = "mysql+mysqldb://{}:{}@{}/{}".format(username, password, hostname, db_name)
        self.__engine = create_engine(db, pool_pre_ping=True, echo=True if env=="test" else False)
        if env == "test":
            Base.metadata.drop_all(self.__engine)
        else:
            Base.metadata.create_all(self.__engine)

        '''session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session)
        self.__session = Session()'''
        
    def all(self, cls=None):
        """query on the current database session (self.__session) all objects
        or depending of the class name"""
        from models.user import User
        from models.city import City
        from models.state import State
        from models.place import Place
        from models.amenity import Amenity
        from models.review import Review

        all_object = (User, State, City, Amenity, Place, Review)
        if cls is not None:
            cls_obj = self.__session.query(cls).all()
            cls_dict = {}
            for obj in cls_obj:
                cls_dict.update({obj.__class__.__name__ + "." + obj.id: obj})
            return cls_dict
        else:
            cls_dict = {}
            for objs in all_object:
                cls_obj = self.__session.query(objs).all()
                for obj in cls_obj:
                    cls_dict.update({obj.__class__.__name__ + "." + obj.id: obj})
            return cls_dict
            

    def new(self, obj):
        """add the object to the current database session (self.__session)"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session (self.__session)"""
        self.__session.commit()

    def delete(self, obj=None):
        """ delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database"""
        from models.user import User
        from models.city import City
        from models.state import State
        from models.place import Place
        from models.amenity import Amenity
        from models.review import Review

        Base.metadata.create_all(bind=self.__engine)
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session)
        self.__session = Session()

