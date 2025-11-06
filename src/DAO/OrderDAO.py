import json
from typing import Dict, List, Optional

from src.Model.Item import Item
from src.Model.Order import Order

from .DBConnector import DBConnector


class OrderDAO:
    """
    DAO for orders where 'items' field is a JSON dictionary of item IDs and quantities.
    """

    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector):
        self.db_connector = db_connector

    def create_order(self, order: Order) -> bool:
        """
        Create a new order with a dictionary of item IDs and quantities.
        :param order: Order object with items as a dictionary {item_id: quantity}.
        :return: True if success.
        """
        try:
            if not isinstance(order.items, dict):
                raise TypeError("Order.items must be a dictionary {item_id: quantity}.")

            for item_id, quantity in order.items.items():
                if not isinstance(item_id, int) or not isinstance(quantity, int):
                    raise TypeError("All item IDs and quantities must be integers.")
                if quantity <= 0:
                    raise ValueError("Quantities must be positive integers.")

            items_json = json.dumps(order.items)
            self.db_connector.sql_query(
                """
                INSERT INTO project_database.orders ( username_customer, username_delivery_driver, address, items)
                VALUES ( %(username_customer)s, %(username_delivery_driver)s, %(address)s, %(items)s);
                RETURNING id_order;""",
                {
                    "username_customer": order.username_customer,
                    "username_delivery_driver": order.username_delivery_driver,
                    "address": order.address,
                    "items": items_json,
                },
                "none",
            )
            return True
        except Exception as e:
            print(f"[OrderDAO] Error creating order: {e}")
            return False

    def find_order_by_id(self, id_order: int) -> Optional[Order]:
        """
        Find order by ID. Loads item IDs and quantities from DB.
        :param id_order: order ID
        :return: Order object with items as a dictionary {item_id: quantity}
        """
        raw_order = self.db_connector.sql_query(
            "SELECT * FROM project_database.orders WHERE id_order = %s;",
            [id_order],
            "one",
        )
        if raw_order is None:
            return None

        items_dict = raw_order.get("items") or ""

        return Order(
            id_order=raw_order["id_order"],
            username_customer=raw_order["username_customer"],
            username_delivery_driver=raw_order["username_delivery_driver"],
            address=raw_order["address"],
            # Pass the dictionary here
            items=items_dict,
        )

    def find_order_by_user(self, username_customer: str) -> Optional[List[Order]]:
        """
        Find orders by the username of the customer.
        :param username_customer: str
        :return: List of Order objects with items as dictionaries {item_id: quantity}
        """
        raw_orders = self.db_connector.sql_query(
            "SELECT * FROM project_database.orders WHERE username_customer = %s;",
            [username_customer],
            "all",
        )
        if not raw_orders:
            return None

        orders = []
        for raw_order in raw_orders:
            # Extract item IDs and quantities from JSON field
            items_dict = json.loads(raw_order.get("items") or "{}")

            # Fetch full Item objects from item IDs
            items = []
            for item_id, quantity in items_dict.items():
                raw_item = self.db_connector.sql_query(
                    "SELECT * FROM items WHERE id_item = %s;",
                    [item_id],
                    "one",
                )
                if raw_item:
                    item = Item(**raw_item)
                    item.quantity = quantity
                    items.append(item)

            orders.append(
                Order(
                    id_order=raw_order["id_order"],
                    username_customer=raw_order["username_customer"],
                    username_delivery_driver=raw_order["username_delivery_driver"],
                    address=raw_order["address"],
                    items=items_dict,  # Return the dictionary of items and quantities
                )
            )

        return orders

    def update(self, order: Order) -> bool:
        """
        Update an order with new details and item IDs and quantities.
        :param order: updated Order object
        :return: True if success
        """
        try:
            if not isinstance(order.items, dict):
                raise TypeError("Order.items must be a dictionary {item_id: quantity}.")

            for item_id, quantity in order.items.items():
                if not isinstance(item_id, int) or not isinstance(quantity, int):
                    raise TypeError("All item IDs and quantities must be integers.")
                if quantity <= 0:
                    raise ValueError("Quantities must be positive integers.")

            items_json = json.dumps(order.items)
            self.db_connector.sql_query(
                """
                UPDATE project_database.orders
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
                    "items": items_json,
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
                "DELETE FROM project_database.orders WHERE id_order = %s;",
                [order.id_order],
                "none",
            )
            return True
        except Exception as e:
            print(f"[OrderDAO] Error deleting order: {e}")
            return False
