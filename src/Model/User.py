from abc import ABC, abstractmethod

from pydantic import BaseModel


class User(BaseModel, ABC):
    username: str
    _firstname: str
    _lastname: str
    _account_type: str
    _password: str
    salt: str

    def __init__(self, username, firstname, lastname, password, salt):
        self.username = username
        self._firstname = firstname
        self._lastname = lastname
        self._password = password
        self._account_type = None
        self.salt = salt

    @property
    def firstname(self):
        """ """
        return self._firstname

    @property
    def lastname(self):
        """ """
        return self._lastname

    @property
    def password(self):
        """ """
        return self._password

    @abstractmethod
    def account_type(self):
        """ """
        pass

    @firstname.setter
    def firstname(self, value):
        """ """
        self._firstname = value

    @lastname.setter
    def edit_lastname(self, value):
        """ """
        self._lastname = value

    @password.setter
    def edit_password(self, value):
        """ """
        self._password = value
