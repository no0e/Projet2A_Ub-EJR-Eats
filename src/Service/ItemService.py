from src.Model.Item import Item
from src.DAO.ItemDAO import ItemDAO
from src.DAO.DBConnector import DBConnector


class ItemService:
    def __init__(self):
        self.db_connector = DBConnector()  # connexion PostgreSQL via ton DBConnector
        self.item_dao = ItemDAO(self.db_connector)


    def create_item(self, name_item, price, category, stock, exposed=False):
        """Create a new item

        Parameters
        -----
        name_item: srt
        price : float
        category: str
        stock : int

        """

        if price < 0:
            raise ValueError("The item price should not be negative.")
        if category not in ("starter", "main course", "dessert", "drink"):
            raise TypeError(
                "The category is not registered. Must be one of: starter, main course, dessert, drink."
            )
        if stock < 0:
            raise ValueError("Stock can't be negative.")

        # Vérifier doublon
        all_exposed = self.item_dao.find_all_item()
        if any(item.name_item.lower() == name_item.lower() for item in all_exposed):
            raise TypeError("The item name is already attributed.")

        # Créer l’item
        new_item = Item(
            id_item=None,  # PostgreSQL générera automatiquement
            name_item=name_item,
            price=price,
            category=category,
            stock=stock,
            exposed=exposed
        )

        success = self.item_dao.create_item(new_item)
        if not success:
            raise ValueError("Failed to create item in the database.")
        return new_item

    def change_name_item(self, old_name, new_name):
        items = self.item_dao.find_all_item()
        if any(item.name_item.lower() == new_name.lower() for item in items):
            raise TypeError("The new name is already attributed.")

        for item in items:
            if item.name_item == old_name:
                item.name_item = new_name
                success = self.item_dao.update(item)
                if not success:
                    raise ValueError("Failed to update the item in the database.")
                return item

        raise TypeError("The item to rename doesn't exist.")

    def delete_item(self, name_delete):
        items = self.item_dao.find_all_exposed_item()
        for item in items:
            if item.name_item.lower() == name_delete.lower():
                success = self.item_dao.delete(item)
                if not success:
                    raise ValueError("Failed to delete the item in the database.")
                return True
        raise TypeError("The item to delete doesn't exist.")

    def modify_price(self, name_item, new_price:float):
        if new_price < 0:
            raise ValueError("The new price can't be negative.")

        items = self.item_dao.find_all_exposed_item()
        for item in items:
            if item.name_item.lower() == name_item.lower():
                item.price = new_price
                success = self.item_dao.update(item)
                if not success:
                    raise ValueError("Failed to update price in the database.")
                return item

        raise TypeError("The item to update doesn't exist.")


    def modify_stock_item(self, name_item, new_stock):
        if new_stock < 0:
            raise ValueError("The stock can't be negative.")
        items = self.item_dao.find_all_exposed_item()
        for item in items:
            if item.name_item.lower() == name_item.lower():
                item.stock = new_stock
                success = self.item_dao.update(item)
                if not success:
                    raise ValueError("Failed to update stock in the database.")
                return item

        raise TypeError("The item to update doesn't exist.")
    def modify_category_item(self, name_item, new_category):
        if new_category not in ("starter", "main course", "dessert", "drink"):
            raise TypeError(
                "The category is not registered. Must be one of: starter, main course, dessert, drink."
            )

        items = self.item_dao.find_all_exposed_item()
        for item in items:
            if item.name_item.lower() == name_item.lower():
                item.category = new_category
                success = self.item_dao.update(item)
                if not success:
                    raise ValueError("Failed to update category in the database.")
                return item

        raise TypeError("The item to update doesn't exist.")


    def expose_item(self, name_item, exposed):
        if exposed not in ("Yes", "No"):
            raise TypeError("The answer should be 'Yes' or 'No'.")

        items = self.item_dao.find_all_exposed_item()
        for item in items:
            if item.name_item.lower() == name_item.lower():
                item.exposed = True if exposed == "Yes" else False
                success = self.item_dao.update(item)
                if not success:
                    raise ValueError("Failed to update exposed status in the database.")
                return item

        raise TypeError("The item to update doesn't exist.")

    def change_availability(self, name_item):
        """ Change if an item is available or not

        Parameters
        ----
        name_item: str
            the item that need to be updated

        Returns
        -----
        Bool
        """
        items = self.item_dao.find_all_item()
        for item in items:
            if item.name_item.lower()== name_item:
                if item.exposed == True:
                    item.exposed = False
                else:
                    item.exposed = True

        raise TypeError("The item to update doesn't exist.")
