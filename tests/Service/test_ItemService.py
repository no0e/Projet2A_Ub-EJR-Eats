import pytest

from src.DAO.DBConnector import DBConnector
from src.DAO.ItemDAO import ItemDAO
from src.Model.Item import Item, ItemCreate
from src.Utils.reset_db import ResetDatabase
from src.Service.ItemService import ItemService

from src.Model.Item import Item


class MockItemRepo:
    def __init__(self):
        self.items = {}
        self.auto_id = 1

    def find_all_item(self):
        return list(self.items.values())

    def find_item_by_name(self, name_item: str):
        for item in self.items.values():
            if item.name_item.lower() == name_item.lower():
                return item
        return None

    def create_item(self, item: Item):
        item.id_item = self.auto_id
        self.auto_id += 1

        for existing in self.items.values():
            if existing.name_item.lower() == item.name_item.lower():
                return False

        self.items[item.id_item] = item
        return True

    def update(self, item: Item):
        if item.id_item not in self.items:
            return False
        self.items[item.id_item] = item
        return True

    def delete(self, item: Item):
        if item and item.id_item in self.items:
            del self.items[item.id_item]
            return True
        return False

    def update_item_exposed(self, id_item: int, exposed: bool):
        if id_item not in self.items:
            return False
        self.items[id_item].exposed = exposed
        return True


item_repo = MockItemRepo()
item_service = ItemService(item_repo)

@pytest.fixture
def item_service():
    repo = MockItemRepo()

    repo.create_item(Item(name_item = "galette saucisse",price = 3.2, category ="main course", stock =102, exposed =True))
    repo.create_item(Item(name_item = "vegetarian galette",
        price = 3.0,
        category = "main dish",
        stock =  30,
        exposed =  False))
    repo.create_item(Item(name_item = "cola",
        price = 2.0,
        category = "drink",
        stock =  501,
        exposed =  True))

    return ItemService(repo)




def test_view_storage(item_service):
    storage = item_service.view_storage()
    assert storage == {"galette saucisse": 102,"vegetarian galette": 30,"cola": 501}

def test_create_item_success(item_service):
    item = item_service.create_item("Burger", 12, "starter", 50)
    assert item.name_item == "Burger"
    assert item.price == 12
    assert item.category == "starter"
    assert item.stock == 50

def test_create_item_failed(item_service):
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

def test_change_name_item_success(item_service):
    item = item_service.change_name_item("galette saucisse", "Pizza")
    assert item.name_item == "Pizza"

def test_change_name_item_failed(item_service):
    with pytest.raises(TypeError) as error_oldname:
        item_service.change_name_item("galette saucisse", "vegetarian galette")
    assert str(error_oldname.value) == "The new name is already attributed."
    with pytest.raises(TypeError) as error_newname:
        item_service.change_name_item("Pizza", "galette")
    assert str(error_newname.value) == "The item to rename doesn't exist."


def test_delete_item_success(item_service):
    item_service.create_item("Pizza", 12, "starter", 50)
    success = item_service.delete_item("Pizza")
    assert success == "The item Pizza is deleted from the database"

def test_delete_item_failed(item_service):
    with pytest.raises(TypeError) as error_name:
        item_service.delete_item("Pizza")
    assert str(error_name.value) == "The item to delete doesn't exist."

def test_modify_price_success(item_service):
    




