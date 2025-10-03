import User
from pydantic import BaseModel


class DeliveryDriver(BaseModel, User):
    username: str
    __firstname__: str
    __lastname__: str
    __account_type__: str
    __password__: str
    salt: str
    __vehicle__: str
    __is_available__: bool

    def __init__(self, username, firstname, lastname, password, salt, vehicle):
        super().__init__(username, firstname, lastname, password, salt)
        self.__account_type__ = "DeliveryDriver"
        self.__vehicle__ = vehicle
        self.__is_available__ = FALSE
