from pydantic import BaseModel

from src.Model.User import User


class DeliveryDriver(User):
    username_delivery_driver: str
    vehicle: str
    is_available: bool
