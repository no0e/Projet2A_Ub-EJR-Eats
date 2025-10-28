from .User import User


class Administrator(User):
    username: str
    _firstname: str
    _lastname: str
    _account_type: str
    _password: str
    salt: str

