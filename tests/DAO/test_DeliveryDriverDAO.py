from typing import List, Optional
import pytest

from src.DAO.DBConnector import DBConnector
from src.DAO.DeliveryDriverDAO import DeliveryDriverDAO
from src.Model.DeliveryDriver import DeliveryDriver


@pytest.fixture
def db_connector():
    db = DBConnector()
    yield db


@pytest.fixture
def delivery_driver_dao(db_connector):
    return DeliveryDriverDAO(db_connector, test=True)

def test_create(delivery_driver_dao):
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
