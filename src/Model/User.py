from abc import ABC, abstractmethod

from pydantic import BaseModel


class User(BaseModel, ABC):
    username: str
    __firstname__: str
    __lastname__: str
    __account_type__: str
    __password__: str
    salt: str

    def __init__(self, username, firstname, lastname, password, salt):
        self.username = username
        self.__firstname__ = firstname
        self.__lastname__ = lastname
        self.__password__ = password
        self.__account_type__ = None
        self.salt = salt

    def get_firstname(self):
        """ """
        # TODO

    def get_lastname(self):
        """ """
        # TODO

    def get_password(self):
        """ """
        pass

    @abstractmethod
    def get_account_type(self):
        """ """
        # TODO

    def edit_firstname(self, firstname):
        """ """
        # TODO

    def edit_lastname(self, lastname):
        """ """
        # TODO

    def edit_password(self, password):
        """ """
        # TODO
