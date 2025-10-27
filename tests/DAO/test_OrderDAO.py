import json
import pytest
from typing import Optional, List
from src.DAO.OrderDAO import OrderDAO
from src.Model.Order import Order
from src.Model.Item import Item

class MockDBConnectorForOrder:
    def __init__(self):
        self.orders = {}
        self.items = {
            1: {"id_item": 1, "name": "Item 1", "price": 10.0, "category": "dessert", "stock": 1, "exposed": False},
            2: {"id_item": 2, "name": "Item 2", "price": 20.0, "category": "starter", "stock": 13, "exposed": True},
        }

    def sql_query(self, query: str, data: dict = None, return_type: str = "one"):
        if "INSERT INTO orders" in query:
            id_order = len(self.orders) + 1
            order_data = {
                "id_order": id_order,
                "username_customer": data["username_customer"],
                "username_delivery_driver": data["username_delivery_driver"],
                "address": data["address"],
                "items": data["items"],
            }
            self.orders[id_order] = order_data
            return None

        elif "SELECT * FROM orders WHERE id_order =" in query:
            id_order = data[0]
            if id_order in self.orders:
                return self.orders[id_order]
            return None

        elif "SELECT * FROM items WHERE id_item =" in query:
            id_item = data[0]
            if id_item in self.items:
                return self.items[id_item]
            return None

        elif "UPDATE orders" in query:
            id_order = data["id_order"]
            if id_order in self.orders:
                self.orders[id_order].update(
                    {
                        "username_customer": data["username_customer"],
                        "username_delivery_driver": data["username_delivery_driver"],
                        "address": data["address"],
                        "items": data["items"],
                    }
                )
            return None

        elif "DELETE FROM orders WHERE id_order =" in query:
            id_order = data[0]
            if id_order in self.orders:
                del self.orders[id_order]
            return None

        return None

def test_create_order():
    mock_db = MockDBConnectorForOrder()
    order_dao = OrderDAO(mock_db)

    items = [Item(id_item=1, name="Item 1", price=10.0, category="dessert", stock=1, exposed=False)]
    order = Order(
        username_customer="alice",
        username_delivery_driver="bob",
        address="123 Main St",
        items=items,
    )

    result = order_dao.create(order)
    assert result is True

def test_find_order():
    mock_db = MockDBConnectorForOrder()
    order_dao = OrderDAO(mock_db)

    items = [Item(id_item=1, name="Item 1", price=10.0, category="dessert", stock=1, exposed=False)]
    order = Order(
        username_customer="alice",
        username_delivery_driver="bob",
        address="123 Main St",
        items=items,
    )
    order_dao.create(order)

    found_order = order_dao.find_order(1)
    assert found_order is not None
    assert found_order.id_order == 1
    assert found_order.username_customer == "alice"
    assert found_order.username_delivery_driver == "bob"
    assert found_order.address == "123 Main St"
    assert len(found_order.items) == 1
    assert found_order.items[0].id_item == 1

def test_update_order():
    mock_db = MockDBConnectorForOrder()
    order_dao = OrderDAO(mock_db)

    items = [Item(id_item=1, name="Item 1", price=10.0, category="dessert", stock=1, exposed=False)]
    order = Order(
        username_customer="alice",
        username_delivery_driver="bob",
        address="123 Main St",
        items=items,
    )
    order_dao.create(order)

    updated_items = [Item(id_item=2, name="Item 2", price=20.0, category="starter", stock=13, exposed=True)]
    updated_order = Order(
        id_order=1,
        username_customer="alice_updated",
        username_delivery_driver="bob_updated",
        address="456 New St",
        items=updated_items,
    )

    result = order_dao.update(updated_order)
    assert result is True

    found_order = order_dao.find_order(1)
    assert found_order.username_customer == "alice_updated"
    assert found_order.username_delivery_driver == "bob_updated"
    assert found_order.address == "456 New St"
    assert len(found_order.items) == 1
    assert found_order.items[0].id_item == 2

def test_delete_order():
    mock_db = MockDBConnectorForOrder()
    order_dao = OrderDAO(mock_db)

    items = [Item(id_item=1, name="Item 1", price=10.0, category="dessert", stock=1, exposed=False)]
    order = Order(
        username_customer="alice",
        username_delivery_driver="bob",
        address="123 Main St",
        items=items,
    )
    order_dao.create(order)

    order_to_delete = Order(id_order=1, username_customer="", username_delivery_driver="", address="", items=[])
    result = order_dao.delete(order_to_delete)
    assert result is True

    found_order = order_dao.find_order(1)
    assert found_order is None

if __name__ == "__main__":
    pytest.main(["-v"])
