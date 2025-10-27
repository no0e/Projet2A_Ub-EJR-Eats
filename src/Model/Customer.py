from src.Model.User import User


class Customer(User):
    username: str
    _firstname: str
    _lastname: str
    _account_type: str
    _password: str
    salt: str
    _address: str

   
