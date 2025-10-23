from src.Model.User import User


class DeliveryDriver(User):
    username: str
    _firstname: str
    _lastname: str
    _account_type: str
    _password: str
    salt: str
    _vehicle: str
    _is_available: bool

    def __init__(self, username, firstname, lastname, password, salt, vehicle):
        super().__init__(username, firstname, lastname, password, salt)
        self._account_type = "DeliveryDriver"
        self._vehicle = vehicle
        self._is_available = False

    @property
    def account_type(self):
        """"""
        return self._account_type

    @property
    def vehicle(self):
        """"""
        return self._vehicle

    @property
    def is_available(self):
        """"""
        return self._is_available

    @vehicle.setter
    def vehicle(self, value):
        """"""
        self._vehicle = value

    @is_available.setter
    def is_available(self, value: bool):
        """"""
        self._is_available = value
