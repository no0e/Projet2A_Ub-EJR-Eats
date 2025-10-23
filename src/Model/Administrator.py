from src.Model.User import User


class Administrator(User):
    username: str
    _firstname: str
    _lastname: str
    _account_type: str
    _password: str
    salt: str

    def __init__(self, username, firstname, lastname, password, salt):
        super().__init__(username, firstname, lastname, password, salt)
        self._account_type = "Administrator"

    @property
    def account_type(self):
        """"""
        return self._account_type
