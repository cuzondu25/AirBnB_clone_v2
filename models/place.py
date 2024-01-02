#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Table
from sqlalchemy.orm import relationship

class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column("city_id", String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column("user_id", String(60), ForeignKey("users.id"), nullable=False)
    name = Column("name", String(128), nullable=False)
    description = Column("description", String(1024), nullable=False)
    number_rooms = Column("number_rooms", Integer, nullable=False, default=0)
    number_bathrooms = Column("number_bathrooms", Integer, nullable=False, default=0)
    max_guest = Column("max_guest", Integer, nullable=False, default=0)
    price_by_night = Column("price_by_night", Integer, nullable=False, default=0)
    latitude = Column("latitude", Float, nullable=False)
    longitude = Column("longitude", Float, nullable=False)
    amenity_ids = []

    place_amenity = Table("place_amenity", Base.metadata,
                          Column("place_id", String(60), ForeignKey('places.id')),
                          Column("amenity_id", String(60), ForeignKey("amenities.id")))

    user = relationship("User", overlaps="places")
    cities = relationship("City")
    reviews = relationship("Review")
    amenities = relationship("Amenity", secondary="place_amenity", viewonly=False)

    @property
    def amenities(self):
        """for FileStorage: getter attribute amenities
        returns:
            the list of Amenity instances based on the attribute amenity_ids
            that contains all Amenity.id linked to the Place
        """
        from models import storage
        from models.amenity import Amenity
        amenity_dict = storage.all(Amenity)
        amenity_list = []
        for amenity_obj in amenity_dict.values():
            for ids in self.amenity_ids:
                if amenity_obj.id == ids:
                    amenity_list.append(amenity_obj)
        return amenity_list
    
    @amenities.setter
    def amenities(self, obj):
        """Setter attribute amenities that handles append method
            for adding an Amenity.id to the attribute amenity_ids.
            This method should accept only Amenity object, otherwise, do nothing.
            """
        from models.amenity import Amenity
        if isinstance(obj, list):
            for ls_obj in obj:
                if isinstance(ls_obj, Amenity):
                    self.amenity_ids.append(ls_obj.id)
        elif isinstance(obj, Amenity):
            self.amenity_ids.append(obj.id)

    @property
    def reviews(self):
        """for FileStorage: getter attribute reviews
        returns:
            the list of Review instances with place_id equals to the current Place.id
        """
        from models import storage
        from models.review import Review
        review_dict = storage.all(Review)
        review_list = []
        for review_obj in review_dict.values():
            if review_obj.place_id == self.id:
                review_list.append(review_obj)
        return review_list
