from typing import List, Optional

from src.Model.DeliveryDriver import DeliveryDriver

from .DBConnector import DBConnector


class DeliveryDriverDAO:
    """
    DAO for DeliveryDriver with minimal delivery_driver table:
    - username_delivery_driver (foreign key to user.username)
    - is_available (bool)
    """

    def __init__(self, db_connector: DBConnector):
        self.db_connector = db_connector

    def create(self, driver: DeliveryDriver) -> bool:
        """
        Create a new entry in delivery_driver table for an existing user.
        """
        try:
            self.db_connector.sql_query(
                """
                INSERT INTO delivery_driver (username_delivery_driver, is_available)
                VALUES (%s, %s);
                """,
                [driver.username, driver.is_available],
                "none",
            )
            return True
        except Exception as e:
            print(f"[DeliveryDriverDAO] Error creating delivery driver: {e}")
            return False

    def find_by_username(self, username: str) -> Optional[DeliveryDriver]:
        """
        Find delivery driver by username joining user and delivery_driver tables.
        """
        raw_driver = self.db_connector.sql_query(
            """
            SELECT u.username, u.firstname, u.lastname, 'DeliveryDriver' as account_type,
                    u.password, u.salt,
                   d.is_available
            FROM user u
            JOIN delivery_driver d ON u.username = d.username_delivery_driver
            WHERE u.username = %s;
            """,
            [username],
            "one",
        )
        if raw_driver is None:
            return None

        # Create DeliveryDriver object from joined data
        driver = DeliveryDriver(
            username=raw_driver["username"],
            firstname=raw_driver["firstname"],
            lastname=raw_driver["lastname"],
            account_type=raw_driver["account_type"],
            password=raw_driver["password"],
            salt=raw_driver["salt"],
            vehicle="",  # You can adapt this if you keep vehicle info elsewhere or ignore
        )
        driver.is_available = raw_driver["is_available"]
        return driver

    def update(self, driver: DeliveryDriver) -> bool:
        """
        Update is_available status in delivery_driver table.
        User info updates are assumed to be handled elsewhere.
        """
        try:
            self.db_connector.sql_query(
                """
                UPDATE delivery_driver
                SET is_available = %s
                WHERE username_delivery_driver = %s;
                """,
                [driver.is_available, driver.username],
                "none",
            )
            return True
        except Exception as e:
            print(f"[DeliveryDriverDAO] Error updating delivery driver: {e}")
            return False

    def delete(self, driver: DeliveryDriver) -> bool:
        """
        Delete delivery driver record from delivery_driver table.
        Does not delete user.
        """
        try:
            self.db_connector.sql_query(
                """
                DELETE FROM delivery_driver
                WHERE username_delivery_driver = %s;
                """,
                [driver.username],
                "none",
            )
            return True
        except Exception as e:
            print(f"[DeliveryDriverDAO] Error deleting delivery driver: {e}")
            return False

    def drivers_available(self) -> List[DeliveryDriver]:
        """
        Return all delivery drivers currently marked as available.
        """
        raw_drivers = self.db_connector.sql_query(
            """
            SELECT u.username, u.firstname, u.lastname, u.password, u.salt,
                   'DeliveryDriver' as account_type,
                   d.is_available
            FROM user u
            JOIN delivery_driver d ON u.username = d.username_delivery_driver
            WHERE d.is_available = TRUE;
            """,
            [],
            "all",
        )
        if not raw_drivers:
            return []

        drivers = []
        for raw_driver in raw_drivers:
            driver = DeliveryDriver(
                username=raw_driver["username"],
                firstname=raw_driver["firstname"],
                lastname=raw_driver["lastname"],
                account_type=raw_driver["account_type"],
                password=raw_driver["password"],
                salt=raw_driver["salt"],
                vehicle="",  # Adjust if needed
            )
            driver.is_available = raw_driver["is_available"]
            drivers.append(driver)
        return drivers
