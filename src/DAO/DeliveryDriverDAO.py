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
            SELECT u.username, d.vehicle, d.is_available
            FROM project_database.users u
            JOIN project_database.delivery_drivers d ON u.username = d.username_delivery_driver
            WHERE u.username = %s
        """
        raw = self.db.sql_query(query, [username], return_type="one")
        return DeliveryDriver(**raw) if raw else None

    def update(self, driver: DeliveryDriver, new_vehicle: str, new_is_available: bool) -> bool:
        query = """
            UPDATE project_database.delivery_drivers
            SET vehicle = %s, is_available = %s
            WHERE username_delivery_driver = %s
        """
        self.db.sql_query(query, [new_vehicle, new_is_available, driver.username], return_type=None)
        return True

    def delete(self, driver: DeliveryDriver) -> bool:
        self.db.sql_query(
            "DELETE FROM project_database.delivery_drivers WHERE username_delivery_driver = %s",
            [driver.username],
        )
        return True

    def drivers_available(self):
        query = """
            SELECT u.username, d.vehicle, d.is_available
            FROM project_database.users u
            JOIN project_database.delivery_drivers d ON u.username = d.username_delivery_driver
            WHERE d.is_available = TRUE
        """
        rows = self.db.sql_query(query, return_type="all")
        return [DeliveryDriver(**r) for r in rows]
