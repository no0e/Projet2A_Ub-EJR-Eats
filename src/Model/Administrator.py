from .User import User


class Administrator(User):
    username: str
    firstname: str
    lastname: str
    password: str
    salt: str
    account_type: str
