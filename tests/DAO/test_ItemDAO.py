from typing import List, Optional

import pytest

from src.DAO.ItemDAO import ItemDAO
from src.Model.Item import Item


class MockDBConnectorForItem:
    def __init__(self):
        self.items = {}
        self.next_id = 1

    def sql_query(self, query: str, data: dict = None, return_type: str = "one"):
        if "INSERT INTO items" in query:
            item_id = self.next_id
            self.next_id += 1
            item_data = {
                "id_item": item_id,
                "name_item": data["name_item"],
                "price": data["price"],
                "category": data["category"],
                "stock": data["stock"],
                "exposed": data["exposed"],
            }
            self.items[item_id] = item_data
            return None

        elif "SELECT * FROM items WHERE id_item =" in query:
            item_id = data[0]
            if item_id in self.items:
                return self.items[item_id]
            return None

        elif "SELECT * FROM items WHERE exposed = TRUE" in query:
            exposed_items = [item for item in self.items.values() if item["exposed"]]
            return exposed_items if return_type == "all" else exposed_items[0] if exposed_items else None

        elif "UPDATE items" in query:
            item_id = data["id_item"]
            if item_id in self.items:
                self.items[item_id].update(
                    {
                        "name_item": data["name_item"],
                        "price": data["price"],
                        "category": data["category"],
                        "stock": data["stock"],
                        "exposed": data["exposed"],
                    }
                )
            return None

        elif "DELETE FROM items WHERE id_item =" in query:
            item_id = data[0]
            if item_id in self.items:
                del self.items[item_id]
            return None

        return None


def test_create_item():
    mock_db = MockDBConnectorForItem()
    item_dao = ItemDAO(mock_db)

    item = Item(
        id_item=None,
        name_item="Galette Saucisse",
        price=3.99,
        category="Main dish",
        stock=50,
        exposed=True,
    )

    result = item_dao.create_item(item)
    assert result is True


def test_find_item():
    mock_db = MockDBConnectorForItem()
    item_dao = ItemDAO(mock_db)

    item = Item(
        id_item=None,
        name_item="Galette Saucisse",
        price=3.99,
        category="Main dish",
        stock=50,
        exposed=True,
    )
    item_dao.create_item(item)

    found_item = item_dao.find_item(1)
    assert found_item is not None
    assert found_item.id_item == 1
    assert found_item.name_item == "Galette Saucisse"
    assert found_item.price == 3.99
    assert found_item.category == "Main dish"
    assert found_item.stock == 50


def test_find_all_exposed_item():
    mock_db = MockDBConnectorForItem()
    item_dao = ItemDAO(mock_db)

    item1 = Item(
        id_item=None,
        name_item="Galette Saucisse",
        price=3.99,
        category="Main dish",
        stock=50,
        exposed=True,
    )
    item2 = Item(
        id_item=None,
        name_item="Banh-Mi",
        price=12.99,
        category="Main dish",
        stock=30,
        exposed=False,
    )
    item_dao.create_item(item1)
    item_dao.create_item(item2)

    exposed_items = item_dao.find_all_exposed_item()
    assert len(exposed_items) == 1
    assert exposed_items[0].name_item == "Galette Saucisse"


def test_update():
    mock_db = MockDBConnectorForItem()
    item_dao = ItemDAO(mock_db)

    item = Item(
        id_item=None,
        name_item="Galette Saucisse",
        price=3.99,
        category="Main dish",
        stock=50,
        exposed=True,
    )
    item_dao.create_item(item)

    updated_item = Item(
        id_item=1,
        name_item="Banh-Mi",
        price=11.99,
        category="Main dish",
        stock=45,
        exposed=True,
    )

    result = item_dao.update(updated_item)
    assert result is True

    found_item = item_dao.find_item(1)
    assert found_item.name_item == "Banh-Mi"
    assert found_item.price == 11.99
    assert found_item.stock == 45


def test_delete():
    mock_db = MockDBConnectorForItem()
    item_dao = ItemDAO(mock_db)

    item = Item(
        id_item=None,
        name_item="Galette Saucisse",
        price=3.99,
        category="Main dish",
        stock=50,
        exposed=True,
    )
    item_dao.create_item(item)

    item_to_delete = Item(id_item=1, name_item="", price=0, category="", stock=0, exposed=False)
    result = item_dao.delete(item_to_delete)
    assert result is True

    found_item = item_dao.find_item(1)
    assert found_item is None


if __name__ == "__main__":
    pytest.main()
