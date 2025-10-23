from src.Model.Item import Item

class ItemService(Item):
    def __init__(self):

    def create_item(self, name, price, category, stock):
        """Create a new item

        Parameters
        -----
        name: srt
        price : int
        category: str
        stock : int

        """

        last_id = max(item['id_item'] for item in Item)
        id_item = last_id + 1
        for item in Item:
            if name==item[name]:
                raise TypeError("The item name pick is already attributed")
        if price < 0:
            raise ValueError("The item price should not be negative")
        if category not in ("starter", "main course", "dessert", "drink"):
            raise TypeError("The category registered is not registered.\
                 You must choose between: starter", "main course", "dessert", "drink ")
        if stock < 0:
            raise ValueError("The stock can't be negative")
        nouvel_item = {
                'id_item': id_item,
                'name': name,
                'price':price,
                'stock':stock}
        items.append(nouvel_item)




