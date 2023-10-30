#!/usr/bin/python3
""" holds class User"""
import models
from hashlib import md5
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

    def __init__(self, *args, **kwargs):
        """user initialize"""
        super().__init__(*args, **kwargs)
        if models.storage_t != 'db':
            self.password = md5(self.password.encode()).hexdigest()

    def to_dict(self, save_to_file=False):
        """Returns a dictionary containing all keys/values of the instance"""
        new_dict = super().to_dict(save_to_file)
        if models.storage_t != 'db' and not save_to_file:
            new_dict["password"] = self.password
        if "password" in new_dict:
            hashed_password = md5(new_dict["password"].encode()).hexdigest()
            new_dict["password"] = hashed_password
        return new_dict
