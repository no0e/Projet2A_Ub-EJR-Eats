import json

import pytest

from src.DAO.DBConnector import DBConnector
from src.DAO.OrderDAO import OrderDAO
from src.Model.Item import Item
from src.Model.Order import Order
from src.Utils.reset_db import ResetDatabase


@pytest.fixture
def db_connector():
    db = DBConnector()
    yield db


@pytest.fixture
def order_dao(db_connector):
    return OrderDAO(db_connector)


def test_create_order(order_dao):
    ResetDatabase().lancer(True)
    # Keys in items dict should be strings (JSON stores keys as strings)
    items = {"1": 2, "3": 1}
    order = Order(
        username_customer="bobbia",
        username_delivery_driver="ernesto",
        address="123 Test St",
        items=items,
    )
    # Pass test=True to use test database
    result = order_dao.create_order(order, test=True)
    assert result is True


def test_find_order_by_id(order_dao):
    ResetDatabase().lancer(True)
    # Pass test=True to use test database
    found_order = order_dao.find_order_by_id(1, test=True)

    assert found_order is not None
    assert found_order.id_order == 1
    assert found_order.username_customer == "bobbia"
    assert found_order.username_delivery_driver == "ernesto1"
    assert found_order.address == "13 Main St."
    # Keys are strings in JSON
    assert found_order.items == {"1": 10}


def test_find_order_by_user(order_dao):
    ResetDatabase().lancer(True)
    # Pass test=True to use test database
    found_orders = order_dao.find_order_by_user("bobbia", test=True)
    no_order = order_dao.find_order_by_user("drdavid", test=True)
    
    assert found_orders is not None
    assert len(found_orders) == 2
    # Check the first order's customer - note: based on your assertion, it seems 
    # the first order for "bobbia" has username_customer "drdavid"? 
    # This seems like it might be a data issue, but keeping your original assertion
    assert found_orders[0].username_customer == "drdavid"
    assert no_order is None


def test_update(order_dao):
    ResetDatabase().lancer(True)
    # items should be a dict, not a JSON string
    future_order = Order(
        id_order=1,
        username_customer="bobbia",
        username_delivery_driver="ernesto1",
        address="51 Rue Blaise Pascal, 35170 Bruz",
        items={"1": 1}  # Dict, not string
    )
    # Pass test=True to use test database
    result = order_dao.update(future_order, test=True)
    assert result is True


if __name__ == "__main__":
    pytest.main()
    ResetDatabase().lancer(True)