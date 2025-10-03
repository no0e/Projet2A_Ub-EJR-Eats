from pydantic import BaseModel


class DeliveryDriver(BaseModel):
    username: str
    firstname: str
    lastname: str
    account_type: str
    password: str
    salt: str
    vehicle: str
    is_available: bool
