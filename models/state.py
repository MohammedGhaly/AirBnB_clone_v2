#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from os import getenv
from sqlalchemy.orm import relationship
from models.city import City
import models


class State(BaseModel, Base):
    """
    a class that represents a state
    Attributes:
    """
    __tablename__ = 'states'

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship('City', backref='state',
                              cascade='all, delete-orphan')
        name = Column(String(128), nullable=False)
    else:
        name = ''
    if getenv("HBNB_TYPE_STORAGE") != 'db':
        @property
        def cities(self):
            """
            Returns the list of `City` instances
            with `state_id` equals to the current
            """
            cities = list()
            for _id, city in models.storage.all(City).items():
                if self.id == city.state_id:
                    cities.append(city)

            return cities
