from typing import Optional

from pydantic import BaseModel

from src.Model.Item import Item


class Order(BaseModel):
    id_order: Optional[int] = None
    username_customer: str
    username_delivery_driver: str
    address: str
    items: list

    @property
    def address(self):
        """"""
        return self._address

    @property
    def items(self):
        """"""
        return self._items

    @address.setter
    def address(self, value):
        """"""
        self.address = value

    @items.setter
    def items(self, value):
        """"""
        self.items = value
