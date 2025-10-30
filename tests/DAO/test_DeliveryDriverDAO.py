from typing import List, Optional

import pytest
from src.DAO.DeliveryDriverDAO import DeliveryDriverDAO

from src.Model.DeliveryDriver import DeliveryDriver


class MockDBConnectorForDeliveryDriver:
    def __init__(self):
        self.delivery_drivers = {}
        self.users = {
            "driver1": {
                "username": "driver1",
                "_firstname": "Alice",
                "_lastname": "Asm",
                "_password": "hashed_password",
                "salt": "salt123",
            },
            "driver2": {
                "username": "driver2",
                "_firstname": "Jane",
                "_lastname": "Smith",
                "_password": "hashed_password2",
                "salt": "salt456",
            },
        }

    def sql_query(self, query: str, data: list = None, return_type: str = "one"):
        if "INSERT INTO delivery_driver" in query:
            username, is_available = data
            self.delivery_drivers[username] = {"username_delivery_driver": username, "is_available": is_available}
            return None

        elif "SELECT" in query and "JOIN delivery_driver" in query:
            if "WHERE u.username" in query:
                username = data[0]
                if username in self.users and username in self.delivery_drivers:
                    user = self.users[username]
                    driver = self.delivery_drivers[username]
                    return {
                        "username": user["username"],
                        "_firstname": user["_firstname"],
                        "_lastname": user["_lastname"],
                        "_password": user["_password"],
                        "salt": user["salt"],
                        "is_available": driver["is_available"],
                    }
                return None
            elif "WHERE d.is_available = TRUE" in query:
                available_drivers = []
                for username, driver in self.delivery_drivers.items():
                    if driver["is_available"]:
                        user = self.users[username]
                        available_drivers.append(
                            {
                                "username": user["username"],
                                "_firstname": user["_firstname"],
                                "_lastname": user["_lastname"],
                                "_password": user["_password"],
                                "salt": user["salt"],
                                "is_available": driver["is_available"],
                            }
                        )
                return (
                    available_drivers if return_type == "all" else available_drivers[0] if available_drivers else None
                )

        elif "UPDATE delivery_driver" in query:
            is_available, username = data
            if username in self.delivery_drivers:
                self.delivery_drivers[username]["is_available"] = is_available
            return None

        elif "DELETE FROM delivery_driver" in query:
            username = data[0]
            if username in self.delivery_drivers:
                del self.delivery_drivers[username]
            return None

        return None


def test_create():
    mock_db = MockDBConnectorForDeliveryDriver()
    driver_dao = DeliveryDriverDAO(mock_db)

    driver = DeliveryDriver(
        username="driver1",
        firstname="Alice",
        lastname="Asm",
        account_type="DeliveryDriver",
        password="hashed_password",
        salt="salt123",
        vehicle="scooter",
        is_available=True,
    )

    result = driver_dao.create(driver)
    assert result is True


def test_find_by_username():
    mock_db = MockDBConnectorForDeliveryDriver()
    driver_dao = DeliveryDriverDAO(mock_db)

    driver = DeliveryDriver(
        username="driver1",
        firstname="Alice",
        lastname="Asm",
        account_type="DeliveryDriver",
        password="hashed_password",
        salt="salt123",
        vehicle="scooter",
        is_available=True,
    )
    driver_dao.create(driver)

    found_driver = driver_dao.find_by_username("driver1")
    assert found_driver is not None
    assert found_driver.username == "driver1"
    assert found_driver.firstname == "Alice"
    assert found_driver.lastname == "Asm"
    assert found_driver.is_available is True


def test_update():
    mock_db = MockDBConnectorForDeliveryDriver()
    driver_dao = DeliveryDriverDAO(mock_db)

    driver = DeliveryDriver(
        username="driver1",
        firstname="Alice",
        lastname="Asm",
        account_type="DeliveryDriver",
        password="hashed_password",
        salt="salt123",
        vehicle="scooter",
        is_available=True,
    )
    driver_dao.create(driver)

    driver.is_available = False
    result = driver_dao.update(driver)
    assert result is True

    found_driver = driver_dao.find_by_username("driver1")
    assert found_driver.is_available is False


def test_delete():
    mock_db = MockDBConnectorForDeliveryDriver()
    driver_dao = DeliveryDriverDAO(mock_db)

    driver = DeliveryDriver(
        username="driver1",
        firstname="Alice",
        lastname="Asm",
        account_type="DeliveryDriver",
        password="hashed_password",
        salt="salt123",
        vehicle="scooter",
        is_available=True,
    )
    driver_dao.create(driver)

    result = driver_dao.delete(driver)
    assert result is True

    found_driver = driver_dao.find_by_username("driver1")
    assert found_driver is None


def test_drivers_available():
    mock_db = MockDBConnectorForDeliveryDriver()
    driver_dao = DeliveryDriverDAO(mock_db)

    driver1 = DeliveryDriver(
        username="driver1",
        firstname="Alice",
        lastname="Asm",
        account_type="DeliveryDriver",
        password="hashed_password",
        salt="salt123",
        vehicle="scooter",
        is_available=True,
    )
    driver2 = DeliveryDriver(
        username="driver2",
        firstname="Jane",
        lastname="Smith",
        account_type="DeliveryDriver",
        password="hashed_password2",
        salt="salt456",
        vehicle="bike",
        is_available=False,
    )
    driver_dao.create(driver1)
    driver_dao.create(driver2)

    available_drivers = driver_dao.drivers_available()
    assert len(available_drivers) == 1
    assert available_drivers[0].username == "driver1"
    assert available_drivers[0].is_available is True


if __name__ == "__main__":
    pytest.main()
