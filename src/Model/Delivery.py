from typing import List, Optional

from pydantic import BaseModel

from src.Model.Order import Order


class Delivery(BaseModel):
    id_delivery: Optional[int] = None
    username_delivery_driver: Optional[str] = None
    duration: Optional[int] = None
    orders: List[Order]
    is_accepted: bool
