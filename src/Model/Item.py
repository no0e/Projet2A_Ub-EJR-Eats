from pydantic import BaseModel


class Item(BaseModel):
    id_item: int
    name: str
    price: float
    category: str
    stock: int
    exposed: bool
