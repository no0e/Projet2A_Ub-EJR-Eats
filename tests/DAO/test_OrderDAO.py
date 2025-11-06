import pytest
import uuid
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
def unique_order_id(db_connector):
    # Generate a unique order ID by inserting a dummy order and then deleting it
    dummy_order_id = db_connector.sql_query(
        """
        INSERT INTO orders (username_customer, username_delivery_driver, address, items)
        VALUES (%s, %s, %s, %s)
        RETURNING id_order;
        """,
        ("dummy_customer", "dummy_driver", "dummy_address", []),
        return_type="one",
    )["id_order"]
    yield dummy_order_id
    # Clean up the dummy order
    db_connector.sql_query(
        "DELETE FROM orders WHERE id_order = %s",
        (dummy_order_id,),
    )

def test_create_order(order_dao, db_connector, unique_username):
    # Insert test items if needed
    item_id = db_connector.sql_query(
        """
        INSERT INTO items (name_item, price, category, stock, exposed)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id_item;
        """,
        ("Test Item", 10.0, "dessert", 1, False),
        return_type="one",
    )["id_item"]

    # Create an order
    items = [Item(id_item=item_id, name_item="Test Item", price=10.0, category="dessert", stock=1, exposed=False)]
    order = Order(
        username_customer=unique_username,
        username_delivery_driver=f"driver_{uuid.uuid4().hex[:8]}",
        address="123 Test St",
        items=items,
    )
    result = order_dao.create(order)
    assert result is True

    # Clean up
    db_connector.sql_query(
        "DELETE FROM orders WHERE username_customer = %s",
        (unique_username,),
    )
    db_connector.sql_query(
        "DELETE FROM items WHERE id_item = %s",
        (item_id,),
    )

def test_find_order(order_dao, db_connector, unique_order_id, unique_username):
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
    db_connector.sql_query(
        """
        INSERT INTO orders (id_order, username_customer, username_delivery_driver, address, items)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (unique_order_id, unique_username, f"driver_{uuid.uuid4().hex[:8]}", "123 Test St", [item_id]),
    )

    # Find the order
    found_order = order_dao.find_order(unique_order_id)
    assert found_order is not None
    assert found_order.id_order == unique_order_id
    assert found_order.username_customer == unique_username

    # Clean up
    db_connector.sql_query(
        "DELETE FROM orders WHERE id_order = %s",
        (unique_order_id,),
    )
    db_connector.sql_query(
        "DELETE FROM items WHERE id_item = %s",
        (item_id,),
    )

def test_update_order(order_dao, db_connector, unique_order_id, unique_username):
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
    db_connector.sql_query(
        """
        INSERT INTO orders (id_order, username_customer, username_delivery_driver, address, items)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (unique_order_id, unique_username, f"driver_{uuid.uuid4().hex[:8]}", "123 Test St", [item_id]),
    )

    # Update the order
    updated_item_id = db_connector.sql_query(
        """
        INSERT INTO items (name_item, price, category, stock, exposed)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id_item;
        """,
        ("Updated Item", 20.0, "starter", 13, True),
        return_type="one",
    )["id_item"]

    updated_order = Order(
        id_order=unique_order_id,
        username_customer=f"{unique_username}_updated",
        username_delivery_driver=f"driver_{uuid.uuid4().hex[:8]}_updated",
        address="456 Updated St",
        items=[Item(id_item=updated_item_id, name_item="Updated Item", price=20.0, category="starter", stock=13, exposed=True)],
    )
    result = order_dao.update(updated_order)
    assert result is True

    # Verify the update
    found_order = order_dao.find_order(unique_order_id)
    assert found_order.username_customer == f"{unique_username}_updated"
    assert found_order.address == "456 Updated St"
    assert len(found_order.items) == 1
    assert found_order.items[0].id_item == updated_item_id

    # Clean up
    db_connector.sql_query(
        "DELETE FROM orders WHERE id_order = %s",
        (unique_order_id,),
    )
    db_connector.sql_query(
        "DELETE FROM items WHERE id_item IN (%s, %s)",
        (item_id, updated_item_id),
    )

def test_delete_order(order_dao, db_connector, unique_order_id, unique_username):
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
    db_connector.sql_query(
        """
        INSERT INTO orders (id_order, username_customer, username_delivery_driver, address, items)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (unique_order_id, unique_username, f"driver_{uuid.uuid4().hex[:8]}", "123 Test St", [item_id]),
    )

    # Delete the order
    order_to_delete = Order(id_order=unique_order_id, username_customer="", username_delivery_driver="", address="", items=[])
    result = order_dao.delete(order_to_delete)
    assert result is True

    # Verify the order is deleted
    found_order = order_dao.find_order(unique_order_id)
    assert found_order is None

    # Clean up the item
    db_connector.sql_query(
        "DELETE FROM items WHERE id_item = %s",
        (item_id,),
    )

if __name__ == "__main__":
    pytest.main()
