from src.Model.User import User


class Customer(User):
    username: str
    firstname: str
    lastname: str
    account_type: str
    password: str
    salt: str
    address: str
