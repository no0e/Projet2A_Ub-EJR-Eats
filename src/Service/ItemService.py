from src.Model.Item import Item


class ItemService(Item):
    def __init__(self):
        self.items = []

    def create_item(self, name, price, category, stock):
        """Create a new item

        Parameters
        -----
        name: srt
        price : int
        category: str
        stock : int

        """

        if self.items:
            last_id = max(item.id_item for item in self.items)
            id_item = last_id + 1
        else:
            id_item = 1

        if any(item.name == name for item in self.items):
            raise TypeError("The item name pick is already attributed")
        if price < 0:
            raise ValueError("The item price should not be negative")
        if category not in ("starter", "main course", "dessert", "drink"):
            raise TypeError(
                "The category registered is not registered.\
                 You must choose between: starter",
                "main course",
                "dessert",
                "drink ",
            )
        if stock < 0:
            raise ValueError("The stock can't be negative")

        new_item = Item(id_item, name, price, category, stock)
        self.items.append(new_item)
        return new_item

    def change_name_item(self, old_name, new_name):
        if any(item.name == new_name for item in self.items):
            raise TypeError("The new name is already attributed.")
        for item in self.items:
            if old_name not in item["name"]:
                raise TypeError("The researched item doesn't exist.")
            else:
                item.name = new_name
            return item

    def delete_item(self, name_delete):
        for item in self.items:
            if item.name == name_delete:
                self.items.remove(item)
            return self.items

    def modify_price(self,name, new_price=int):
        if new_price < 0:
            raise ValueError("The new price is not correct. It can't be neagtive.")
        for item in self.items:
            if item.name == name:
                item.price = new_price
                return item

    def modify_stock_item(name, new_stock):
        if new_stock < 0:
            raise ValueError("The stock can't be neagtive")
        for item in Item:
            if name in item["name"]:
                item["stock"] = new_stock
        return Item

    def modify_category_item(name, new_category):
        if new_category not in ("starter", "main course", "dessert", "drink"):
            raise TypeError(
                "The category registered is not registered.\
                 You must choose between: starter",
                "main course",
                "dessert",
                "drink ",
            )
        for item in Item:
            if name in item["name"]:
                item["category"] = new_category
        return Item
