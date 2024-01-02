#!/usr/bin/python3
""" Amenity Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class Amenity(BaseModel, Base):
    from models.place import Place
    __tablename__ = "amenities"
    name = Column("name", String(128), nullable=False)
    
    places = relationship("Place", secondary="place_amenity")
