from typing import Optional

from src.DAO.UserDAO import UserDAO
from src.Model.DeliveryDriver import DeliveryDriver


class DeliveryDriverDAO(UserDAO):
    def __init__(self, db_connector):
        super().__init__(db_connector)
        self.db = db_connector

    def create(self, driver: DeliveryDriver) -> bool:
        raw_created_driver = self.db.sql_query(
            """
            INSERT INTO delivery_drivers (username_delivery_driver, vehicle, is_available)
            VALUES (%(username_delivery_driver)s, %(vehicle)s, %(is_available)s)
            RETURNING *;
            """,
            {
                "username_delivery_driver": driver.username,
                "vehicle": driver.vehicle,
                "is_available": driver.is_available,
            },
            "one",
        )
        return raw_created_driver is not None

    def find_by_username(self, username: str):
        query = """
            SELECT d.username_delivery_driver as username, u.firstname, u.lastname, u.salt, u.account_type, u.password, d.vehicle, d.is_available
            FROM delivery_drivers as d
            JOIN users as u ON u.username = username
            WHERE username = %s
        """
        raw = self.db.sql_query(query, [username], return_type="one")
        return DeliveryDriver(**raw) if raw else None

    def update_delivery_driver(
        self, username: str, vehicle: Optional[str] = None, is_available: Optional[bool] = None
    ) -> bool:
        if vehicle is None:
            vehicle = self.find_by_username(username).vehicle
        if is_available is None:
            is_available = self.find_by_username(username).is_available
        query = """
            UPDATE delivery_drivers
            SET vehicle = %(vehicle)s, is_available = %(is_available)s
            WHERE username_delivery_driver = %(username)s
        """
        self.db.sql_query(
            query, {"username": username, "vehicle": vehicle, "is_available": is_available}, return_type=None
        )
        return True

    def delete(self, driver: DeliveryDriver) -> bool:
        self.db.sql_query(
            "DELETE FROM delivery_drivers WHERE username_delivery_driver = %s",
            [driver.username],
        )
        return True

    def drivers_available(self):
        query = """
            SELECT username_delivery_driver, vehicle, is_available
            FROM delivery_drivers
            WHERE is_available = TRUE
        """
        rows = self.db.sql_query(query, return_type="all")
        return [DeliveryDriver(**r) for r in rows]
