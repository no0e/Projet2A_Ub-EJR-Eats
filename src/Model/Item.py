from typing import Optional

from pydantic import BaseModel


class Item(BaseModel):
    id_item: Optional[int]
    name: str
    price: float
    category: str
    stock: int
    exposed: bool = False
