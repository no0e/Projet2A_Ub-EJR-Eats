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
    return ItemService(db_connector=db_connector)



def test_view_storage(item_service ):
    ResetDatabase.lancer(True)
    storage = item_service.view_storage()
    assert storage == {"galette saucisse": 102,"vegetarian galette": 30,"cola": 501}

def test_create_item_success(item_service):
    ResetDatabase.lancer(True)
    item = item_service.create_item("Burger", 12, "starter", 50)
    assert item.name_item == "Burger"
    assert item.price == 12
    assert item.category == "starter"
    assert item.stock == 50

def test_create_item_failed(item_service):
    ResetDatabase.lancer(True)
    with pytest.raises(ValueError) as error_price:
        item_service.create_item("Pizza", -12, "starter", 50)
    assert str(error_price.value) == "The item price should not be negative."
    with pytest.raises(TypeError) as error_category:
        item_service.create_item("Pizza", 12, "dish", 50)
    assert str(error_category.value) == "The category is not registered. Must be one of: starter, main course, dessert, drink."
    with pytest.raises(ValueError) as error_stock:
        item_service.create_item("Pizza", 12, "starter", -50)
    assert str(error_stock.value) == "Stock can't be negative."
    with pytest.raises(TypeError) as error_name:
        item_service.create_item("galette saucisse", 12, "starter", 50)
    assert str(error_name.value) == "The item name is already attributed."







