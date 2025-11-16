import json
from typing import List

from src.DAO.OrderDAO import OrderDAO
from src.Model.Delivery import Delivery
from src.Model.Order import Order

from .DBConnector import DBConnector

db_connector = DBConnector()
order_dao = OrderDAO(db_connector)


class DeliveryDAO:
    def __init__(self, db_connector: DBConnector, test: bool = False):
        self.db = db_connector
        if test:
            self.schema = "project_test_database"
        else:
            self.schema = "project_database"

    def create(self, delivery: Delivery) -> bool:
        id_orders = [order.id_order for order in delivery.orders]
        stops = [order.address for order in delivery.orders]
        query = (
            """
            INSERT INTO """
            + self.schema
            + """.deliveries
            (username_delivery_driver, duration, id_orders, stops, is_accepted)
            VALUES ( %(username_delivery_driver)s, %(duration)s, %(id_orders)s, %(stops)s, %(is_accepted)s)
            RETURNING id_delivery;
        """
        )
        try:
            self.db.sql_query(
                query,
                {
                    "id_delivery": delivery.id_delivery,
                    "username_delivery_driver": delivery.username_delivery_driver,
                    "duration": delivery.duration,
                    "id_orders": id_orders,
                    "stops": stops,
                    "is_accepted": delivery.is_accepted,
                },
            )
            return True
        except Exception as e:
            print(f"[DeliveryDAO] Error creating delivery: {e}")
            return False

    def get_available_deliveries(self) -> List[Delivery]:
        query = "SELECT * FROM " + self.schema + ".deliveries WHERE is_accepted = FALSE;"
        rows = self.db.sql_query(query, return_type="all")
        deliveries = []
        for r in rows:
            orders = [order_dao.find_order_by_id(order_id) for order_id in r["id_orders"]]
            deliveries.append(
                Delivery(
                    id_delivery=r["id_delivery"],
                    username_delivery_driver=r["username_delivery_driver"],
                    duration=r["duration"],
                    orders=orders,
                    is_accepted=r["is_accepted"],
                )
            )
        return deliveries

    def get_by_id(self, id_delivery: int):
        query = "SELECT * FROM " + self.schema + ".deliveries WHERE id_delivery = %(id_delivery)s"
        row = self.db.sql_query(query, {"id_delivery": id_delivery}, return_type="one")
        return Delivery(**row) if row else None

    def set_delivery_accepted(self, id_delivery: int, username_driver: str):
        query = (
            """
            UPDATE """
            + self.schema
            + """.deliveries
            SET is_accepted = TRUE, username_delivery_driver = %(username)s
            WHERE id_delivery = %(id_delivery)s AND is_accepted = FALSE
        """
        )
        self.db.sql_query(query, {"id_delivery": id_delivery, "username": username_driver})
