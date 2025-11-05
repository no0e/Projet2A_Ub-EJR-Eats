from src.Model.User import User


class Customer(User):
    username: str
    firstname: str
    lastname: str
    password: str
    salt: str
    account_type: str
    address: str
