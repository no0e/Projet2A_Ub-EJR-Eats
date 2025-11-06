import pytest
from src.DAO.ItemDAO import ItemDAO
from src.Model.Item import ItemCreate
from src.DAO.DBConnector import DBConnector
from src.Utils.reset_db import ResetDatabase

@pytest.fixture
def db_connector():
    db = DBConnector()
    yield db

@pytest.fixture
def item_dao(db_connector):
    return ItemDAO(db_connector)

@pytest.fixture(scope="module")
def reset_db_teardown():
    """
    A fixture that yields control to the test function,
    and then automatically resets the test database afterward.
    """
    print("\n[TEARDOWN] Resetting database...")
    ResetDatabase().lancer()
    print("[TEARDOWN] Database reset complete.")

    # 1. Setup Phase: The test runs here
    # The 'yield' keyword separates setup from teardown.
    yield


def test_create_item(item_dao, reset_db_teardown):
    item = ItemCreate(
        "galette test",
        "4",
        "main dish",
        1000,
        True
    )
    result = item_dao.create_item(item)
    assert result is True

def test_update_item_exposed(item_dao, reset_db_teardown):
    #The item 1 has exposed=True
    item_dao.update_item_exposed(1,False)
    #The item 2 already has exposed=False
    item_dao.update_item_exposed(2,False)
    assert item_dao.find_item(1).exposed is False
    assert item_dao.find_item(2).exposed is False

def test_find_item(item_dao, reset_db_teardown):
    item = item_dao.find_item(1)
    missing_item = item_dao.find_item(56)
    assert item.id_item == 1
    assert item.name_item == 'galette saucisse'
    assert item.price == 3.2
    assert item.category == 'main dish'
    assert item.stock == 102
    assert item.exposed is False
    assert missing_item is None

def test_find_item_by_name(item_dao, reset_db_teardown):
    item = item_dao.find_item_by_name('galette saucisse')
    missing_item = item_dao.find_item_by_name('disgusting galette')
    assert item.id_item == 1
    assert item.name_item == 'galette saucisse'
    assert item.price == 3.2
    assert item.category == 'main dish'
    assert item.stock == 102
    assert item.exposed is False
    assert missing_item is None

def test_all_exposed_item(item_dao, reset_db_teardown):
    exposed_items = item_dao.find_all_exposed_item()
    assert isinstance(exposed_items, list)
    assert len(exposed_items) == 2
    assert exposed_items[1].id_item == 3

if __name__ == "__main__":
    pytest.main()
