#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column("name", String(128), nullable=True)
    cities = relationship("City", back_populates="states")

    @property
    def cities(self):
        return (relationship(City, where(State.id = City.state_id, backref="states")))