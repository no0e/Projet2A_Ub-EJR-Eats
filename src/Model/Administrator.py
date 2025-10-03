import User
from pydantic import BaseModel


<<<<<<< HEAD
class Administrator(BaseModel, User):
=======
class Administrator(BaseModel):
>>>>>>> 905c3609387dc125116ba7d5475deafe15803420
    username: str
    __firstname__: str
    __lastname__: str
    __account_type__: str
    __password__: str
    salt: str

    def __init__(self, username, firstname, lastname, password, salt):
        super().__init__(username, firstname, lastname, password, salt)
        self.__account_type__ = "Administrator"

    
