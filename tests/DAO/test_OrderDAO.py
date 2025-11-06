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


def test_create_order(order_dao, test=True):
    ResetDatabase().lancer(True)
    items = {"1": 2, "3":1}
    order = Order(
        username_customer="bobbia",
        username_delivery_driver="ernesto",
        address="123 Test St",
        items=items,
    )
    result = order_dao.create_order(order)
    assert result is True


def test_find_order_by_id(order_dao):
    ResetDatabase().lancer(True)
    found_order = order_dao.find_order_by_id(1)

    assert found_order is not None
    assert found_order.id_order == 1
    assert found_order.username_customer == "bobbia"
    assert found_order.username_delivery_driver == "ernesto1"
    assert found_order.address == "13 Main St."
    assert found_order.items == {"1": 10}

def test_find_order_by_user(order_dao):
    ResetDatabase().lancer(True)
    found_orders = order_dao.find_order_by_user("bobbia")
    no_order = order_dao.find_order_by_user("drdavid")
    assert found_orders is not None
    assert len(found_orders) == 2
    assert found_orders[0].username_customer == "drdavid"
    assert no_order is None

def test_update(order_dao, test=True):
    ResetDatabase().lancer(True)
    future_order = Order(
        id_order=1,
        username_customer="bobbia",
        username_delivery_driver="ernesto1",
        address="51 Rue Blaise Pascal, 35170 Bruz",
        items='{"1":1}'
    )
    result = order_dao.update(future_order)
    assert result is True

if __name__ == "__main__":
    pytest.main()
    ResetDatabase().lancer(True)
