from typing import Optional, Dict

from pydantic import BaseModel

from src.Model.Item import Item


class Order(BaseModel):
    id_order: Optional[int] = None
    username_customer: str
    username_delivery_driver: str
    address: str
    items: Dict[str, int]
