from src.Model.User import User


class DeliveryDriver(User):
    username: str
    firstname: str
    lastname: str
    account_type: str
    password: str
    salt: str
    vehicle: str
    is_available: bool = True
