from typing import List, Optional

from src.Model.Item import Item

from .DBConnector import DBConnector


class ItemDAO:
    """
    Data Access Object (DAO) for interacting with the 'items' table in the database.
    Provides CRUD (Create, Read, Update, Delete) operations for Item objects.
    """

    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector):
        """
        Initialize the ItemDAO with a database connector.

        :param db_connector: Instance of DBConnector used to execute SQL queries.
        """
        self.db_connector = db_connector

    def create_item(self, item: Item) -> bool:
        """
        Insert a new item into the database.

        :param item: The Item object to insert.
        :return: True if insertion succeeded, False otherwise.
        """
        try:
            self.db_connector.sql_query(
                """
                INSERT INTO items (id_item, name, price, category, stock, exposed)
                VALUES (DEFAULT, %(name)s, %(price)s, %(category)s, %(stock)s, %(exposed)s);
                """,
                {
                    "name": item.name,
                    "price": item.price,
                    "category": item.category,
                    "stock": item.stock,
                    "exposed": item.exposed,
                },
                "none",
            )
            return True
        except Exception as e:
            print(f"[ItemDAO] Error creating item: {e}")
            return False

    def find_item(self, id_item: int) -> Optional[Item]:
        """
        Retrieve a single item by its ID.

        :param id_item: The ID of the item to find.
        :return: An Item object if found, otherwise None.
        """
        raw_item = self.db_connector.sql_query("SELECT * FROM items WHERE id_item = %s;", [id_item], "one")

        if raw_item is None:
            return None

        return Item(
            id_item=raw_item["id_item"],
            name=raw_item["name"],
            price=raw_item["price"],
            category=raw_item["category"],
            stock=raw_item["stock"],
        )

    def find_all_exposed_item(self) -> List[Item]:
        """
        Retrieve all items marked as exposed (available for customers).

        :return: A list of Item objects that are exposed.
        """
        raw_items = self.db_connector.sql_query("SELECT * FROM items WHERE exposed = TRUE;", [], "all")

        return [
            Item(
                id_item=row["id_item"],
                name=row["name"],
                price=row["price"],
                category=row["category"],
                stock=row["stock"],
            )
            for row in raw_items
        ]

    def update(self, item: Item) -> bool:
        """
        Update an existing item in the database.

        :param item: The Item object containing updated data.
        :return: True if update succeeded, False otherwise.
        """
        try:
            self.db_connector.sql_query(
                """
                UPDATE items
                SET name = %(name)s,
                    price = %(price)s,
                    category = %(category)s,
                    stock = %(stock)s,
                    exposed = %(exposed)s
                WHERE id_item = %(id_item)s;
                """,
                {
                    "id_item": item.id_item,
                    "name": item.name,
                    "price": item.price,
                    "category": item.category,
                    "stock": item.stock,
                    "exposed": item.exposed,
                },
                "none",
            )
            return True
        except Exception as e:
            print(f"[ItemDAO] Error updating item: {e}")
            return False

    def delete(self, item: Item) -> bool:
        """
        Delete an item from the database.

        :param item: The Item object to delete.
        :return: True if deletion succeeded, False otherwise.
        """
        try:
            self.db_connector.sql_query("DELETE FROM items WHERE id_item = %s;", [item.id_item], "none")
            return True
        except Exception as e:
            print(f"[ItemDAO] Error deleting item: {e}")
            return False
