from typing import List, Optional

import pytest

from src.DAO.DBConnector import DBConnector
from src.DAO.DeliveryDAO import DeliveryDAO
from src.Model.Delivery import Delivery
from src.Utils.reset_db import ResetDatabase


@pytest.fixture
def db_connector():
    db = DBConnector()
    yield db

@pytest.fixture
def delivery_dao(db_connector):
    return DeliveryDAO(db_connector, test=True)


def test_create(delivery_dao):
    ResetDatabase().lancer(True)
    created_delivery = Delivery(
        username_delivery_driver="ernesto",
        duration=40,
        id_order = [3,4],
        stops = ['13 Main St.', '4 Salty Spring Av.'],
        is_accepted = False
    )
    creation = delivery_dao.create(created_delivery)
    assert creation is True
    with pytest.raises(TypeError):
        delivery_dao.create(1)

def test_get_available_deliveries(delivery_dao):
    ResetDatabase().lancer(True)
    available_deliveries = delivery_dao.get_available_deliveries()
    assert len(available_deliveries) == 1

def test_get_by_id(delivery_dao):
    ResetDatabase().lancer(True)
    delivery = delivery_dao.get_by_id(1)
    assert delivery.username_delivery_driver == "ernesto"
    assert delivery.duration == 50
    assert delivery.id_orders == [1,2]
    assert delivery.stops == ['13 Main St.', '4 Salty Spring Av.']
    assert delivery.is_accepted is True
    with pytest.raises(TypeError):
        delivery_dao.get_by_id("1")

def test_set_delivery_accepted(delivery_dao):
    id_delivery = 2
    username_delivery_driver = "ernesto1"
    duration = 15
    update = delivery_dao.set_delivery_accepted(
        id_delivery=id_delivery,
        username_delivery_driver=username_delivery_driver,
        duration=duration
    )
    assert update is None
    updated_delivery = delivery_dao.get_by_id(2)
    assert updated_delivery.is_accepted is True

if __name__ == "__main__":
    pytest.main()
    ResetDatabase().lancer(True)
