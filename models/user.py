#!/usr/bin/python3
""" holds class User"""
import models
import hashlib
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user",
                              cascade="all, delete, delete-orphan")
        reviews = relationship("Review", backref="user",
                               cascade="all, delete, delete-orphan")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def init(self, *args, **kwargs):
        """Initialization of the user model"""
        super().init(*args, **kwargs)
        if models.storage_t != 'db':
            self.password = hashlib.md5(self.password.encode()).hexdigest()

    def to_dict(self, save_password=False):
        """Returns a dictionary containing all keys/values of the instance"""
        new_dict = self.dict.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        new_dict["class"] = self.class.__name
        if not save_password and "password" in new_dict:
            del new_dict["password"]
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        return new_dict

    def save(self):
        """Updates the attribute 'updated_at' with the current datetime and saves the data"""
        self.updated_at = datetime.utcnow()
        if models.storage_t != 'db':
            models.storage.new(self)
            models.storage.save()
