from typing import List, Optional

from src.Model.Item import ItemCreate, Item

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
            raw_item = self.db_connector.sql_query(
            """
            INSERT INTO project_database.items (name_item, price, category, stock, exposed)
            VALUES (%(name_item)s, %(price)s, %(category)s, %(stock)s, %(exposed)s)
            RETURNING id_item;
            """,
                {
                    "name_item": item.name_item,
                    "price": item.price,
                    "category": item.category,
                    "stock": item.stock,
                    "exposed": item.exposed,
                },
                "one",
            )
            item.id_item = raw_item["id_item"]
            return True
        except Exception as e:
            print(f"[ItemDAO] Error creating item: {e}")
            raise e  # ou print(e)

    def update_item_exposed(self, id_item, exposed):
        """Met à jour l'exposition de l'item dans la base de données"""
        query = """
        UPDATE project_database.items
        SET exposed = %s
        WHERE id_item = %s
        """
        self.db_connector.sql_query(query, [exposed, id_item], "execute")

    def find_item(self, id_item: int) -> Optional[Item]:
        """
        Retrieve a single item by its ID.

        :param id_item: The ID of the item to find.
        :return: An Item object if found, otherwise None.
        """
        raw_item = self.db_connector.sql_query(
            "SELECT * FROM project_database.items WHERE id_item = %s;", [id_item], "one"
        )

        if raw_item is None:
            return None

        return Item(
            id_item=raw_item["id_item"],
            name_item=raw_item["name_item"],
            price=raw_item["price"],
            category=raw_item["category"],
            stock=raw_item["stock"],
        )

    def find_item_by_name(self, name_item: str) -> Optional[Item]:
        """
        Retrieve a single item by its name.

        :param name_item: The ID of the item to find.
        :return: An Item object if found, otherwise None.
        """
        raw_item = self.db_connector.sql_query(
            "SELECT * FROM project_database.items WHERE name_item = %s;", [name_item], "one"
        )

        if raw_item is None:
            return None

        return Item(
            id_item=raw_item["id_item"],
            name_item=raw_item["name_item"],
            price=raw_item["price"],
            category=raw_item["category"],
            stock=raw_item["stock"],
        )

    def find_all_exposed_item(self) -> List[Item]:
        """
        Retrieve all items marked as exposed (available for customers).

        :return: A list of Item objects that are exposed.
        """
        raw_items = self.db_connector.sql_query("SELECT * FROM project_database.items WHERE exposed = TRUE;", [], "all")

        return [
            Item(
                id_item=row["id_item"],
                name_item=row["name_item"],
                price=row["price"],
                category=row["category"],
                stock=row["stock"],
            )
            for row in raw_items
        ]

    def find_all_item(self) -> List[Item]:
        """
        Retrieve all items marked as exposed (available for customers).

        :return: A list of Item objects that are exposed.
        """
        raw_items = self.db_connector.sql_query("SELECT * FROM project_database.items ", [], "all")

        return [
            Item(
                id_item=row["id_item"],
                name_item=row["name_item"],
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
                UPDATE project_database.items
                SET name_item = %(name_item)s,
                    price = %(price)s,
                    category = %(category)s,
                    stock = %(stock)s,
                    exposed = %(exposed)s
                WHERE id_item = %(id_item)s;
                """,
                {
                    "id_item": item.id_item,
                    "name_item": item.name_item,
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
            self.db_connector.sql_query(
                "DELETE FROM project_database.items WHERE id_item = %s;", [item.id_item], "none"
            )
            return True
        except Exception as e:
            print(f"[ItemDAO] Error deleting item: {e}")
            return False
