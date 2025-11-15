from typing import List, Optional
import pytest

from src.Utils.reset_db import ResetDatabase
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
    ResetDatabase().lancer(True)
    driver_to_create = DeliveryDriver(
        username="new_driver",
        firstname="Greg",
        lastname="Good",
        account_type="DeliveryDriver",
        password="hashedpassword",
        salt="salt123",
        vehicle="scooter",
        is_available=True,
    )
    missing_driver = None
    assert delivery_driver_dao.create(driver_to_create)
    assert not delivery_driver_dao.create(missing_driver)

def test_find_by_username(delivery_driver_dao):
    ResetDatabase().lancer(True)
    found_driver = delivery_driver_dao.find_by_username("ernesto")
    assert found_driver is not None
    assert found_driver.username == "ernesto"
    assert found_driver.vehicle == "car"
    assert not found_driver.is_available

def test_update_delivery_driver(delivery_driver_dao):
    ResetDatabase().lancer(True)
    to_be_updated_driver = delivery_driver_dao.find_by_username("ernesto1")
    updated_driver = delivery_driver_dao.update_delivery_driver(to_be_updated_driver, vehicle="car")
    missing_driver = None
    no_updated_driver = delivery_driver_dao.update_delivery_driver(missing_driver)
    assert updated_driver
    assert not no_updated_driver


def test_update():
    ...

def test_delete():
    ...


def test_drivers_available():
    ...


if __name__ == "__main__":
    pytest.main()
