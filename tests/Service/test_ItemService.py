import pytest

from src.DAO.DBConnector import DBConnector
from src.DAO.ItemDAO import ItemDAO
from src.Model.Item import Item, ItemCreate
from src.Utils.reset_db import ResetDatabase
from src.Service.ItemService import ItemService


@pytest.fixture
def db_connector():
    db = DBConnector()
    yield db


@pytest.fixture
def item_service(db_connector):
    return ItemService(test=True)

def test_view_storage(item_service ):
    ResetDatabase.lancer(True)
    storage = item_service.view_storage()
    assert storage == {"galette saucisse": 102,"vegetarian galette": 30,"cola": 501}
