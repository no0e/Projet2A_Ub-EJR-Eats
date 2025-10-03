import Item
from pydantic import BaseModel


class Order(BaseModel):
    id_order: int
    username_customer: str
    username_delivery_driver: str
    address: str
    items: list(Item)
