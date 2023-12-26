#!/usr/bin/python3
""" SQL storage engine"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base_model import Base




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
        db_storage = getenv("HBNB_TYPE_STORAGE")    # the type of storage used. It can be “file” (using FileStorage) or db (using DBStorage
        
        db = "mysql+mysqldb://{}:{}@{}/{}".format(username, password, hostname, db_name)
        self.__engine = create_engine(db, pool_pre_ping=True, echo=True if env=="test" else False)
        if env == "test":
            Base.metadata.drop_all(self.__engine)
        else:
            Base.metadata.create_all(self.__engine)

        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session)
        self.__session = Session()
        
    def all(self, cls=None):
        all_object = (User, State, City, Amenity, Place, Review)
        if cls is not None:
            cls_obj = self.__session.query(cls)
            cls_dict = {}
            for obj in cls_obj:
                cls_dict.update({cls + "." + obj.id: obj})
            return cls_dict
        else:
            all_obj = self.__session.query(all_object)
            return all_obj

