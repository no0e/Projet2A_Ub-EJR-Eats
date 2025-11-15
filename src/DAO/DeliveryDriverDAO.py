from typing import Optional

from src.DAO.UserDAO import UserDAO
from src.Model.DeliveryDriver import DeliveryDriver


class DeliveryDriverDAO(UserDAO):
    def __init__(self, db_connector, test: bool = False):
        super().__init__(db_connector, test)

    def create(self, driver: DeliveryDriver) -> bool:
        if not isinstance(driver, DeliveryDriver):
            raise TypeError("The created driver must be of a type driver.")
        if self.get_by_username(driver.username) is not None:
            raise ValueError(f"Username {driver.username} is already taken.")
        raw_created_driver = self.db_connector.sql_query(
            """
            INSERT INTO """
            + self.schema
            + """.delivery_drivers (username_delivery_driver, vehicle, is_available)
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
        query = (
            """
            SELECT d.username_delivery_driver as username, u.firstname, u.lastname, u.salt, u.account_type, u.password, d.vehicle, d.is_available
            FROM """
            + self.schema
            + """.delivery_drivers as d
            JOIN users as u ON u.username = username
            WHERE username = %s
        """
        )
        raw = self.db_connector.sql_query(query, [username], return_type="one")
        return DeliveryDriver(**raw) if raw else None

    def update_delivery_driver(
        self, username: str, vehicle: Optional[str] = None, is_available: Optional[bool] = None
    ) -> bool:
        current_driver = self.find_by_username(username)
        if not isinstance(current_driver, DeliveryDriver):
            return False

        vehicle = vehicle if vehicle is not None else current_driver.vehicle
        is_available = is_available if is_available is not None else current_driver.is_available

        set_clause = []
        params = {"username": username}

        if vehicle != current_driver.vehicle:
            set_clause.append("vehicle = %(vehicle)s")
            params["vehicle"] = vehicle

        if is_available != current_driver.is_available:
            set_clause.append("is_available = %(is_available)s")
            params["is_available"] = is_available

        if not set_clause:
            return False

        query = (
            """UPDATE """
            + self.schema
            + f""".delivery_drivers
            SET {", ".join(set_clause)}"""
            f"""WHERE username_delivery_driver = %(username)s
        """
        )
        self.db_connector.sql_query(query, params, return_type=None)

        return True

    def delete(self, driver: DeliveryDriver) -> bool:
        self.db_connector.sql_query(
            "DELETE FROM " + self.schema + ".delivery_drivers WHERE username_delivery_driver = %s",
            [driver.username],
        )
        return True

    def drivers_available(self):
        query = (
            """
            SELECT username_delivery_driver, vehicle, is_available
            FROM """
            + self.schema
            + """.delivery_drivers
            WHERE is_available = TRUE
        """
        )
        rows = self.db_connector.sql_query(query, return_type="all")
        return [DeliveryDriver(**r) for r in rows]
