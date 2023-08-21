#!/usr/bin/bash
"""a module containing DBStorage class to manage database storage"""
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
# from models.amenity import Amenity
from models.place import Place
from models.review import Review
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

defined_classes = {"State", "City", "Amenity", "User", "Place", "Review"}


class DBStorage:
    """
    DBStorage class to manage database storage
    """

    __engine = None
    __session = None

    def __init__(self):
        """inirializes the SQLAlchemy engine"""
        url = "{0}+{1}://{2}:{3}@{4}:3306/{5}".format(
            'mysql', 'mysqldb', getenv('HBNB_MYSQL_USER'),
            getenv('HBNB_MYSQL_PWD'), getenv('HBNB_MYSQL_HOST'),
            getenv('HBNB_MYSQL_DB'))
        self.__engine = create_engine(url, pool_pre_ping=True)
        self.reload()

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        queries all objects depending on the class name
        """
        data = dict()

        if cls:
            return self.retrieve_data(cls, data)

        for entity in defined_classes:
            data = self.retrieve_data(eval(entity), data)

        return data

    def new(self, obj):
        """
        Add a new object to the current database session
        """
        if obj:
            self.__session.add(obj)

    def save(self):
        """
        Commits the changes to the database session.
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        deletes an object from the database session
        """

        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
        creates all tables in the database and creates the database session
        """

        Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine,
                               expire_on_commit=False)
        Session = scoped_session(factory)
        self.__session = Session()

    def retrieve_data(self, cls, data_dict):
        """
        Gets the data from MySQL database Table
        fills data_dict with the data retrieved
        """

        if type(data_dict) is dict:
            query = self.__session.query(cls)

            for _row in query.all():
                key = "{}.{}".format(cls.__name__, _row.id)
                data_dict[key] = _row

            return data_dict

    def close(self):
        """closes the Session"""
        self.__session.close()
