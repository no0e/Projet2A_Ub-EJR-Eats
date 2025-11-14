import json
from typing import Dict, List, Optional

from src.Model.Item import Item
from src.Model.Order import Order

from .DBConnector import DBConnector


class OrderDAO:
    """
    DAO pour les commandes.
    Le champ 'items' est un dictionnaire {nom_item: quantité}.
    """

    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector):
        self.db_connector = db_connector

    def create_order(self, order: Order, test: bool = False) -> bool:
        """Créer une commande dans la DB."""
        try:
            schema = "project_test_database" if test else "project_database"
            if not isinstance(order.items, dict):
                raise TypeError("Order.items must be a dictionary {item_name: quantity}.")

            for item_name, quantity in order.items.items():
                if not isinstance(item_name, str) or not isinstance(quantity, int):
                    raise TypeError("All item names must be strings and quantities integers.")
                if quantity <= 0:
                    raise ValueError("Quantities must be positive integers.")

            items_json = json.dumps(order.items)
            self.db_connector.sql_query(
                f"""
                INSERT INTO {schema}.orders (username_customer, username_delivery_driver, address, items)
                VALUES (%(username_customer)s, %(username_delivery_driver)s, %(address)s, %(items)s)
                RETURNING id_order;
                """,
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

    def find_order_by_id(self, id_order: int, test: bool = False) -> Optional[Order]:
        """Trouver une commande par son ID."""
        schema = "project_test_database" if test else "project_database"
        raw_order = self.db_connector.sql_query(
            f"SELECT * FROM {schema}.orders WHERE id_order = %s;",
            [id_order],
            "one",
        )
        if raw_order is None:
            return None

        raw_items = raw_order.get("items") or {}
        items_dict = json.loads(raw_items) if isinstance(raw_items, str) else raw_items

        return Order(
            id_order=raw_order["id_order"],
            username_customer=raw_order["username_customer"],
            username_delivery_driver=raw_order["username_delivery_driver"],
            address=raw_order["address"],
            items=items_dict,
        )

    def find_order_by_user(self, username_customer: str, test: bool = False) -> Optional[List[Order]]:
        """Trouver toutes les commandes d'un utilisateur."""
        schema = "project_test_database" if test else "project_database"
        raw_orders = self.db_connector.sql_query(
            f"SELECT * FROM {schema}.orders WHERE username_customer = %s;",
            [username_customer],
            "all",
        )
        if not raw_orders:
            return None

        orders = []
        for raw_order in raw_orders:
            raw_items = raw_order.get("items") or {}
            items_dict = json.loads(raw_items) if isinstance(raw_items, str) else raw_items

            orders.append(
                Order(
                    id_order=raw_order["id_order"],
                    username_customer=raw_order["username_customer"],
                    username_delivery_driver=raw_order["username_delivery_driver"],
                    address=raw_order["address"],
                    items=items_dict,
                )
            )
        return orders

    def update(self, order: Order, test: bool = False) -> bool:
        """Mettre à jour une commande."""
        try:
            schema = "project_test_database" if test else "project_database"

            for item_name, quantity in order.items.items():
                if not isinstance(item_name, str) or not isinstance(quantity, int):
                    raise TypeError("All item names must be strings and quantities integers.")
                if quantity <= 0:
                    raise ValueError("Quantities must be positive integers.")

            items_json = json.dumps(order.items)
            self.db_connector.sql_query(
                f"""
                UPDATE {schema}.orders
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

    def delete(self, order: Order, test: bool = False) -> bool:
        """Supprimer une commande."""
        try:
            schema = "project_test_database" if test else "project_database"
            self.db_connector.sql_query(
                f"DELETE FROM {schema}.orders WHERE id_order = %s;",
                [order.id_order],
                "none",
            )
            return True
        except Exception as e:
            print(f"[OrderDAO] Error deleting order: {e}")
            return False
