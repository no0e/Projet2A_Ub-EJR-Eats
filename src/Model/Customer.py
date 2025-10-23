from src.Model.User import User


class Customer(User):
    username: str
    _firstname: str
    _lastname: str
    _account_type: str
    _password: str
    salt: str
    _address: str

    def __init__(self, username, firstname, lastname, password, salt, address):
        super().__init__(username, firstname, lastname, password, salt)
        self._account_type = "Customer"
        self._address = address

    @property
    def account_type(self):
        """"""
        return self._account_type

    @property
    def address(self):
        """"""
        return self._address

    @address.setter
    def address(self, value):
        """"""
        self._address = value
