import Item
from pydantic import BaseModel


class Order(BaseModel):
    id_order: int
    username_customer: str
    username_delivery_driver: str
    address: str
    items: list(Item)

    def __init__(self, id_order, username_customer, username_delivery_driver, address, items):
        self.id_order = id_order
        self.username_customer = username_customer
        self.username_delivery_driver = username_delivery_driver
        self._address = address
        self._items = items

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
