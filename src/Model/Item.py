from pydantic import BaseModel


class Item(BaseModel):
    id_item: int
    name: str
    price: float
    category: str
    stock: int
    exposed: bool

    def __init__(self, id_item, name, price, category, stock):
        self.id_item = id_item
        self._name = name
        self._price = price
        self._category = category
        self._stock = stock
        self._exposed = False

    @property
    def name(self):
        """"""
        return self._name

    @property
    def price(self):
        """"""
        return self._price

    @property
    def category(self):
        """"""
        return self._category

    @property
    def stock(self):
        """"""
        return self._stock

    @property
    def exposed(self):
        """"""
        return self._exposed

    @name.setter
    def name(self, value):
        """"""
        self.name = value

    @price.setter
    def price(self, value):
        """"""
        self.price = value

    @category.setter
    def category(self, value):
        """"""
        self.category = value

    @stock.setter
    def stock(self, value):
        """"""
        self.stock = value

    @exposed.setter
    def exposed(self, value: bool):
        """"""
        self.exposed = value
