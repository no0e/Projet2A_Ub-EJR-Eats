import pytest
import uuid
import json
from src.DAO.OrderDAO import OrderDAO
from src.Model.Item import Item
from src.Model.Order import Order
from src.DAO.DBConnector import DBConnector

@pytest.fixture
def db_connector():
    db = DBConnector()
    yield db

@pytest.fixture
def order_dao(db_connector):
    return OrderDAO(db_connector)

@pytest.fixture
def unique_username():
    return f"user_{uuid.uuid4().hex[:8]}"

@pytest.fixture
def unique_driver_username():
    return f"driver_{uuid.uuid4().hex[:8]}"

def test_create_order(order_dao):
    items = '{"1": 2, "3":1}'
    order = Order(
        username_customer=unique_username,
        username_delivery_driver=unique_driver_username,
        address="123 Test St",
        items=items,
    )
    result = order_dao.create_order(order)
    assert result is True


def test_find_order_by_id(order_dao):
    found_order = order_dao.find_order_by_id(1)
    
    assert found_order is not None
    assert found_order.id_order == 1
    assert found_order.username_customer == 'bobbia'
    assert found_order.username_delivery_driver == 'ernesto1'
    assert found_order.address == '13 Main St.'
    assert found_order.items == {"1":10}


def test_find_order_by_user(order_dao, db_connector, unique_username, unique_driver_username):
    # Insert a test user for customer
    db_connector.sql_query(
        """
        INSERT INTO users (username, firstname, lastname, password, salt, account_type)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (unique_username, "Test", "User", "hashedpassword", "salt123", "Customer"),
    )

    # Insert a test user for delivery driver
    db_connector.sql_query(
        """
        INSERT INTO users (username, firstname, lastname, password, salt, account_type)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (unique_driver_username, "Test", "Driver", "hashedpassword", "salt123", "DeliveryDriver"),
    )

    # Insert a test item
    item_id = db_connector.sql_query(
        """
        INSERT INTO items (name_item, price, category, stock, exposed)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id_item;
        """,
        ("Test Item", 10.0, "dessert", 1, False),
        return_type="one",
    )["id_item"]

    # Insert a test order
    items = {item_id: 2}
    db_connector.sql_query(
        """
        INSERT INTO orders (username_customer, username_delivery_driver, address, items)
        VALUES (%s, %s, %s, %s)
        """,
        (unique_username, unique_driver_username, "123 Test St", json.dumps(items)),
    )

    # Find the order by user
    found_orders = order_dao.find_order_by_user(unique_username)
    assert found_orders is not None
    assert len(found_orders) > 0
    assert found_orders[0].username_customer == unique_username
    assert found_orders[0].items == items

    # Clean up
    db_connector.sql_query(
        f"DELETE FROM orders WHERE username_customer = %s",
        (unique_username,),
    )
    db_connector.sql_query(
        f"DELETE FROM users WHERE username IN (%s, %s)",
        (unique_username, unique_driver_username),
    )
    db_connector.sql_query(
        f"DELETE FROM items WHERE id_item = %s",
        (item_id,),
    )

def test_update(order_dao, db_connector, unique_username, unique_driver_username):
    # Insert a test user for customer
    db_connector.sql_query(
        """
        INSERT INTO users (username, firstname, lastname, password, salt, account_type)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (unique_username, "Test", "User", "hashedpassword", "salt123", "Customer"),
    )

    # Insert a test user for delivery driver
    db_connector.sql_query(
        """
        INSERT INTO users (username, firstname, lastname, password, salt, account_type)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (unique_driver_username, "Test", "Driver", "hashedpassword", "salt123", "DeliveryDriver"),
    )

    # Insert test items
    item_id = db_connector.sql_query(
        """
        INSERT INTO items (name_item, price, category, stock, exposed)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id_item;
        """,
        ("Test Item", 10.0, "dessert", 1, False),
        return_type="one",
    )["id_item"]

    updated_item_id = db_connector.sql_query(
        """
        INSERT INTO items (name_item, price, category, stock, exposed)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id_item;
        """,
        ("Updated Item", 20.0, "starter", 13, True),
        return_type="one",
    )["id_item"]

    # Insert a test order
    items = {item_id: 2}
    order_id = db_connector.sql_query(
        """
        INSERT INTO orders (username_customer, username_delivery_driver, address, items)
        VALUES (%s, %s, %s, %s)
        RETURNING id_order;
        """,
        (unique_username, unique_driver_username, "123 Test St", json.dumps(items)),
        return_type="one",
    )["id_order"]

    # Update the order
    updated_items = {updated_item_id: 3}
    updated_order = Order(
        id_order=order_id,
        username_customer=f"{unique_username}_updated",
        username_delivery_driver=f"{unique_driver_username}_updated",
        address="456 Updated St",
        items=updated_items,
    )
    result = order_dao.update(updated_order)
    assert result is True

    # Verify the update
    found_order = order_dao.find_order_by_id(order_id)
    assert found_order.username_customer == f"{unique_username}_updated"
    assert found_order.address == "456 Updated St"
    assert found_order.items == updated_items

    # Clean up
    db_connector.sql_query(
        f"DELETE FROM orders WHERE id_order = %s",
        (order_id,),
    )
    db_connector.sql_query(
        f"DELETE FROM users WHERE username IN (%s, %s, %s, %s)",
        (unique_username, unique_driver_username, f"{unique_username}_updated", f"{unique_driver_username}_updated"),
    )
    db_connector.sql_query(
        f"DELETE FROM items WHERE id_item IN (%s, %s)",
        (item_id, updated_item_id),
    )

def test_delete(order_dao, db_connector, unique_username, unique_driver_username):
    # Insert a test user for customer
    db_connector.sql_query(
        """
        INSERT INTO users (username, firstname, lastname, password, salt, account_type)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (unique_username, "Test", "User", "hashedpassword", "salt123", "Customer"),
    )

    # Insert a test user for delivery driver
    db_connector.sql_query(
        """
        INSERT INTO users (username, firstname, lastname, password, salt, account_type)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (unique_driver_username, "Test", "Driver", "hashedpassword", "salt123", "DeliveryDriver"),
    )

    # Insert a test item
    item_id = db_connector.sql_query(
        """
        INSERT INTO items (name_item, price, category, stock, exposed)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id_item;
        """,
        ("Test Item", 10.0, "dessert", 1, False),
        return_type="one",
    )["id_item"]

    # Insert a test order
    items = {item_id: 2}
    order_id = db_connector.sql_query(
        """
        INSERT INTO orders (username_customer, username_delivery_driver, address, items)
        VALUES (%s, %s, %s, %s)
        RETURNING id_order;
        """,
        (unique_username, unique_driver_username, "123 Test St", json.dumps(items)),
        return_type="one",
    )["id_order"]

    # Delete the order
    order_to_delete = Order(id_order=order_id, username_customer="", username_delivery_driver="", address="", items={})
    result = order_dao.delete(order_to_delete)
    assert result is True

    # Verify the order is deleted
    found_order = order_dao.find_order_by_id(order_id)
    assert found_order is None

    # Clean up
    db_connector.sql_query(
        f"DELETE FROM users WHERE username IN (%s, %s)",
        (unique_username, unique_driver_username),
    )
    db_connector.sql_query(
        f"DELETE FROM items WHERE id_item = %s",
        (item_id,),
    )

if __name__ == "__main__":
    pytest.main()
