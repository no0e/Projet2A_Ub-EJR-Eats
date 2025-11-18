from typing import List, Optional

import pytest

from src.DAO.DBConnector import DBConnector
from src.DAO.UserDAO import DeliveryDAO
from src.DAO.DeliveryDriverDAO import DeliveryDriverDAO
from src.Model.DeliveryDriver import DeliveryDriver
from src.Utils.reset_db import ResetDatabase


@pytest.fixture
def db_connector():
    db = DBConnector()
    yield db

@pytest.fixture
def delivery_dao(db_connector):
    return DeliveryDAO(db_connector, test=True)


def test_create(delivery_dao):
  ...


if __name__ == "__main__":
    pytest.main()
    ResetDatabase().lancer(True)
