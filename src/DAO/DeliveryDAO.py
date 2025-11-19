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
        id_orders = delivery.id_orders
        stops = delivery.stops
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
        rows = self.db.sql_query(query, return_type="all") or []
        return [Delivery(**r) for r in rows]

    def get_by_id(self, id_delivery: int):
        query = "SELECT * FROM " + self.schema + ".deliveries WHERE id_delivery = %(id_delivery)s"
        row = self.db.sql_query(query, {"id_delivery": id_delivery}, return_type="one")
        stops_raw = row.get("stops")
        if isinstance(stops_raw, str):
            stops = stops_raw.strip("{}").split(",")
        elif isinstance(stops_raw, list):
            stops = stops_raw
        else:
            stops = []
        delivery = Delivery(
            id_delivery=row["id_delivery"],
            username_delivery_driver=row["username_delivery_driver"],
            duration=row["duration"],
            id_orders=row["id_orders"],
            stops=stops,
            is_accepted=row["is_accepted"],
        )
        return delivery if row else None

    def set_delivery_accepted(self, id_delivery: int, username_driver: str, duration: int):
        query = (
            """
            UPDATE """
            + self.schema
            + """.deliveries
            SET is_accepted = TRUE, username_delivery_driver = %(username_driver)s, duration = %(duration)s
            WHERE id_delivery = %(id_delivery)s AND is_accepted = FALSE
        """
        )
        self.db.sql_query(query, {"id_delivery": id_delivery, "username_driver": username_driver, "duration": duration})

        id_order = self.get_by_id(id_delivery).id_orders[-1]
        query = (
            """
            UPDATE """
            + self.schema
            + """.orders
            SET username_delivery_driver = %(username_driver)s
            WHERE id_order = %(id_order)s
        """
        )
        self.db.sql_query(query, {"id_order": id_order, "username_driver": username_driver})
