import pytest
import uuid
from src.DAO.UserDAO import UserDAO
from src.Model.User import User
from src.DAO.DBConnector import DBConnector

@pytest.fixture
def db_connector():
    db = DBConnector()
    yield db

@pytest.fixture
def user_dao(db_connector):
    return UserDAO(db_connector)

@pytest.fixture
def unique_username():
    # Generate a unique username for each test
    return f"testuser_{uuid.uuid4().hex[:8]}"

def test_get_by_username(user_dao, db_connector, unique_username):
    # Insert a user for this test
    db_connector.sql_query(
        """
        INSERT INTO users (username, firstname, lastname, password, salt, account_type)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (unique_username, "Test", "User", "hashedpassword", "salt123", "Customer"),
    )
    # Run the test
    user = user_dao.get_by_username(unique_username)
    assert user is not None
    assert user.username == unique_username
    assert user.firstname == "Test"
    assert user.lastname == "User"
    assert user.account_type == "Customer"
    # Clean up
    db_connector.sql_query(
        "DELETE FROM users WHERE username = %s",
        (unique_username,),
    )

def test_create_user(user_dao, db_connector, unique_username):
    new_user = User(
        username=unique_username,
        firstname="New",
        lastname="User",
        password="newhashedpassword",
        salt="newsalt",
        account_type="Customer",
    )
    assert user_dao.create_user(new_user) is True
    created_user = user_dao.get_by_username(unique_username)
    assert created_user is not None
    assert created_user.firstname == "New"
    assert created_user.lastname == "User"
    # Clean up
    db_connector.sql_query(
        "DELETE FROM users WHERE username = %s",
        (unique_username,),
    )

def test_update_user(user_dao, db_connector, unique_username):
    # Insert a user for this test
    db_connector.sql_query(
        """
        INSERT INTO users (username, firstname, lastname, password, salt, account_type)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (unique_username, "Test", "User", "hashedpassword", "salt123", "Customer"),
    )
    # Run the test
    assert user_dao.update_user(unique_username, firstname="UpdatedFirst", lastname="UpdatedLast") is True
    updated_user = user_dao.get_by_username(unique_username)
    assert updated_user.firstname == "UpdatedFirst"
    assert updated_user.lastname == "UpdatedLast"
    # Clean up
    db_connector.sql_query(
        "DELETE FROM users WHERE username = %s",
        (unique_username,),
    )

def test_delete_user(user_dao, db_connector, unique_username):
    # Insert a user for this test
    db_connector.sql_query(
        """
        INSERT INTO users (username, firstname, lastname, password, salt, account_type)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (unique_username, "Test", "User", "hashedpassword", "salt123", "Customer"),
    )
    # Run the test
    user = user_dao.get_by_username(unique_username)
    assert user_dao.delete_user(user) is True
    assert user_dao.get_by_username(unique_username) is None
    # No need to clean up, as the user is already deleted

if __name__ == "__main__":
    pytest.main()
