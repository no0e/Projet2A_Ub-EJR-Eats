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
                "firstname": "Alice",
                "lastname": "Asm",
                "password": "hashedpassword",
                "salt": "salt123",
                "account_type": "DeliveryDriver",
            },
            "driver2": {
                "username": "driver2",
                "firstname": "Jane",
                "lastname": "Smith",
                "password": "hashedpassword2",
                "salt": "salt456",
                "account_type": "DeliveryDriver",
            },
        }

    def sql_query(self, query: str, data: list = None, return_type: str = "one"):
        # CREATE
        if "INSERT INTO delivery_driver" in query:
            username, vehicle, is_available = data
            self.delivery_drivers[username] = {
                "username_delivery_driver": username,
                "vehicle": vehicle,
                "is_available": is_available,
            }
            return None

        # FIND BY USERNAME
        elif "SELECT" in query and "JOIN delivery_driver" in query:
            if "WHERE u.username" in query:
                username = data[0]
                if username in self.users and username in self.delivery_drivers:
                    user = self.users[username]
                    driver = self.delivery_drivers[username]
                    return {
                        "username": user["username"],
                        "firstname": user["firstname"],
                        "lastname": user["lastname"],
                        "password": user["password"],
                        "salt": user["salt"],
                        "account_type": user["account_type"],
                        "vehicle": driver["vehicle"],
                        "is_available": driver["is_available"],
                    }
                return None

            elif "WHERE d.is_available = TRUE" in query:
                available = []
                for username, driver in self.delivery_drivers.items():
                    if driver["is_available"]:
                        user = self.users[username]
                        available.append({
                            "username": user["username"],
                            "firstname": user["firstname"],
                            "lastname": user["lastname"],
                            "password": user["password"],
                            "salt": user["salt"],
                            "account_type": user["account_type"],
                            "vehicle": driver["vehicle"],
                            "is_available": driver["is_available"],
                        })
                return available if return_type == "all" else available[0] if available else None

        # UPDATE
        elif "UPDATE delivery_driver" in query:
            vehicle, is_available, username = data
            if username in self.delivery_drivers:
                self.delivery_drivers[username]["vehicle"] = vehicle
                self.delivery_drivers[username]["is_available"] = is_available
            return None

        # DELETE
        elif "DELETE FROM delivery_driver" in query:
            username = data[0]
            if username in self.delivery_drivers:
                del self.delivery_drivers[username]
            return None

        return None


# ---- TESTS ----

def test_create():
    mock_db = MockDBConnectorForDeliveryDriver()
    dao = DeliveryDriverDAO(mock_db)

    driver = DeliveryDriver(
        username="driver1",
        firstname="Alice",
        lastname="Asm",
        account_type="DeliveryDriver",
        password="hashedpassword",
        salt="salt123",
        vehicle="scooter",
        is_available=True,
    )

    assert dao.create(driver) is True
    assert "driver1" in mock_db.delivery_drivers


def test_find_by_username():
    mock_db = MockDBConnectorForDeliveryDriver()
    dao = DeliveryDriverDAO(mock_db)

    driver = DeliveryDriver(
        username="driver1",
        firstname="Alice",
        lastname="Asm",
        account_type="DeliveryDriver",
        password="hashedpassword",
        salt="salt123",
        vehicle="scooter",
        is_available=True,
    )
    dao.create(driver)

    found = dao.find_by_username("driver1")
    assert found is not None
    assert found.username == "driver1"
    assert found.vehicle == "scooter"
    assert found.is_available is True


def test_update():
    mock_db = MockDBConnectorForDeliveryDriver()
    dao = DeliveryDriverDAO(mock_db)

    driver = DeliveryDriver(
        username="driver1",
        firstname="Alice",
        lastname="Asm",
        account_type="DeliveryDriver",
        password="hashedpassword",
        salt="salt123",
        vehicle="scooter",
        is_available=True,
    )
    dao.create(driver)
    driver.vehicle = "car"
    driver.is_available = False
    assert dao.update(driver) is True

    found = dao.find_by_username("driver1")
    assert found.vehicle == "car"
    assert found.is_available is False


def test_delete():
    mock_db = MockDBConnectorForDeliveryDriver()
    dao = DeliveryDriverDAO(mock_db)

    driver = DeliveryDriver(
        username="driver1",
        firstname="Alice",
        lastname="Asm",
        account_type="DeliveryDriver",
        password="hashedpassword",
        salt="salt123",
        vehicle="scooter",
        is_available=True,
    )
    dao.create(driver)
    assert dao.delete(driver) is True
    assert dao.find_by_username("driver1") is None


def test_drivers_available():
    mock_db = MockDBConnectorForDeliveryDriver()
    dao = DeliveryDriverDAO(mock_db)

    driver1 = DeliveryDriver(
        username="driver1",
        firstname="Alice",
        lastname="Asm",
        account_type="DeliveryDriver",
        password="hashedpassword",
        salt="salt123",
        vehicle="scooter",
        is_available=True,
    )
    driver2 = DeliveryDriver(
        username="driver2",
        firstname="Jane",
        lastname="Smith",
        account_type="DeliveryDriver",
        password="hashedpassword2",
        salt="salt456",
        vehicle="bike",
        is_available=False,
    )

    dao.create(driver1)
    dao.create(driver2)

    available = dao.drivers_available()
    assert len(available) == 1
    assert available[0].username == "driver1"
    assert available[0].vehicle == "scooter"


if __name__ == "__main__":
    pytest.main()
