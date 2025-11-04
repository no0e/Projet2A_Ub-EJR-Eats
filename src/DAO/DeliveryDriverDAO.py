from src.Model.DeliveryDriver import DeliveryDriver
from src.DAO.UserDAO import UserDAO


class DeliveryDriverDAO(UserDAO):
    def __init__(self, db_connector):
        super().__init__(db_connector)
        self.db_connector = db_connector

    def create(self, driver: DeliveryDriver) -> bool:
        try:
            self.db_connector.sql_query(
                """
                INSERT INTO delivery_driver (username_delivery_driver, vehicle, is_available)
                VALUES (?, ?, ?)
                """,
                [driver.username, driver.vehicle, driver.is_available],
            )
            return True
        except Exception as e:
            print(f"[DeliveryDriverDAO] Error creating delivery driver: {e}")
            return False

    def find_by_username(self, username: str):
        try:
            raw = self.db_connector.sql_query(
                """
                SELECT u.username, u.firstname, u.lastname, u.password, u.salt, 
                       u.account_type, d.vehicle, d.is_available
                FROM users u
                JOIN delivery_driver d ON u.username = d.username_delivery_driver
                WHERE u.username = ?
                """,
                [username],
            )
            if not raw:
                return None
            return DeliveryDriver(**raw)
        except Exception as e:
            print(f"[DeliveryDriverDAO] Error finding delivery driver: {e}")
            return None

    def update(self, driver: DeliveryDriver) -> bool:
        try:
            self.db_connector.sql_query(
                """
                UPDATE delivery_driver
                SET vehicle = ?, is_available = ?
                WHERE username_delivery_driver = ?
                """,
                [driver.vehicle, driver.is_available, driver.username],
            )
            return True
        except Exception as e:
            print(f"[DeliveryDriverDAO] Error updating delivery driver: {e}")
            return False

    def delete(self, driver: DeliveryDriver) -> bool:
        try:
            self.db_connector.sql_query(
                """
                DELETE FROM delivery_driver
                WHERE username_delivery_driver = ?
                """,
                [driver.username],
            )
            return True
        except Exception as e:
            print(f"[DeliveryDriverDAO] Error deleting delivery driver: {e}")
            return False

    def drivers_available(self):
        try:
            rows = self.db_connector.sql_query(
                """
                SELECT u.username, u.firstname, u.lastname, u.password, u.salt, 
                       u.account_type, d.vehicle, d.is_available
                FROM users u
                JOIN delivery_driver d ON u.username = d.username_delivery_driver
                WHERE d.is_available = TRUE
                """,
                return_type="all",
            )
            return [DeliveryDriver(**r) for r in rows] if rows else []
        except Exception as e:
            print(f"[DeliveryDriverDAO] Error listing available drivers: {e}")
            return []
