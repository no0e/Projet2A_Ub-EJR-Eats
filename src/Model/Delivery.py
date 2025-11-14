from typing import List

from pydantic import BaseModel

from src.Model.Order import Order


class Delivery(BaseModel):
    id_delivery: int
    username_driv: str
    duration: int
    orders: List[Order]
