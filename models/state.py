#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column("name", String(128), nullable=False)
     
    cities = relationship("City")

    @property
    def cities(self):
        """for FileStorage: getter attribute cities
        returns:
            the list of City instances with state_id equals to the current State.id
        """
        from models import storage
        from models.city import City
        city_dict = storage.all(City)
        city_list = []
        for city_obj in city_dict.values():
            if city_obj.id == self.id:
                city_list.append(city_obj)
        return city_list
