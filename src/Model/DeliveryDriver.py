from src.Model.User import User


class DeliveryDriver(User):
    username: str
    firstname: str
    lastname: str
    account_type: str
    password: str
    salt: str
    vehicle: str
    is_available: bool

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
