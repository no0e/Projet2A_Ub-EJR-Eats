from .User import User


class Administrator(User):
    username: str
    firstname: str
    lastname: str
    account_type: str
    password: str
    salt: str

