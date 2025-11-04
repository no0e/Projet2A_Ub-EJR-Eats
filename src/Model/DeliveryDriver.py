from pydantic import BaseModel
from src.Model.User import User

class DeliveryDriver(User):
    vehicle: str
    is_available: bool
