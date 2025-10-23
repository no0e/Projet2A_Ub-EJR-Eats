import json
from typing import Optional

from src.Model.Item import Item
from src.Model.Order import Order

from .DBConnector import DBConnector


class OrderDAO:
    """
    DAO for orders where 'items' field is a JSON list of item IDs (ints).
    """

    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector):
        self.db_connector = db_connector

    def create(self, order: Order) -> bool:
        """
        Create a new order with a list of item IDs.

        :param order: Order object with items as list of Item objects.
        :return: True if success.
        """
        try:
            # Extract item IDs from Item objects
            item_ids = [item.id_item for item in order.items]

            self.db_connector.sql_query(
                """
                INSERT INTO orders (id_order, username_customer, username_delivery_driver, address, items)
                VALUES (DEFAULT, %(username_customer)s, %(username_delivery_driver)s, %(address)s, %(items)s);
                """,
                {
                    "username_customer": order.username_customer,
                    "username_delivery_driver": order.username_delivery_driver,
                    "address": order.address,
                    "items": json.dumps(item_ids),
                },
                "none",
            )
            return True
        except Exception as e:
            print(f"[OrderDAO] Error creating order: {e}")
            return False

    def find_order(self, id_order: int) -> Optional[Order]:
        """
        Find order by ID. Loads item IDs from DB.

        :param id_order: order ID
        :return: Order object with items as full Item objects
        """
        raw_order = self.db_connector.sql_query(
            "SELECT * FROM orders WHERE id_order = %s;",
            [id_order],
            "one",
        )
        if raw_order is None:
            return None

        # Extract item IDs from JSON field
        item_ids = json.loads(raw_order.get("items") or "[]")

        # Fetch full Item objects from item IDs
        # Assuming you have ItemDAO or similar to fetch items by IDs
        items = []
        for item_id in item_ids:
            raw_item = self.db_connector.sql_query(
                "SELECT * FROM items WHERE id_item = %s;",
                [item_id],
                "one",
            )
            if raw_item:
                items.append(Item(**raw_item))

        return Order(
            id_order=raw_order["id_order"],
            username_customer=raw_order["username_customer"],
            username_delivery_driver=raw_order["username_delivery_driver"],
            address=raw_order["address"],
            items=items,
        )

    def update(self, order: Order) -> bool:
        """
        Update an order with new details and item IDs.

        :param order: updated Order object
        :return: True if success
        """
        try:
            item_ids = [item.id_item for item in order.items]
            self.db_connector.sql_query(
                """
                UPDATE orders
                SET username_customer = %(username_customer)s,
                    username_delivery_driver = %(username_delivery_driver)s,
                    address = %(address)s,
                    items = %(items)s
                WHERE id_order = %(id_order)s;
                """,
                {
                    "id_order": order.id_order,
                    "username_customer": order.username_customer,
                    "username_delivery_driver": order.username_delivery_driver,
                    "address": order.address,
                    "items": json.dumps(item_ids),
                },
                "none",
            )
            return True
        except Exception as e:
            print(f"[OrderDAO] Error updating order: {e}")
            return False

    def delete(self, order: Order) -> bool:
        """
        Delete order by id.

        :param order: Order object
        :return: True if success
        """
        try:
            self.db_connector.sql_query(
                "DELETE FROM orders WHERE id_order = %s;",
                [order.id_order],
                "none",
            )
            return True
        except Exception as e:
            print(f"[OrderDAO] Error deleting order: {e}")
            return False
