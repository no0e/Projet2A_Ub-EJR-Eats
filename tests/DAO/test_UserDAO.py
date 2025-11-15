import pytest
import uuid
from src.DAO.UserDAO import UserDAO
from src.Model.User import User
from src.DAO.DBConnector import DBConnector
from src.Utils.reset_db import ResetDatabase

@pytest.fixture
def db_connector():
    db = DBConnector()
    yield db

@pytest.fixture
def user_dao(db_connector):
    return UserDAO(db_connector, test=True)


def test_get_by_username(user_dao):
    ResetDatabase().lancer(True)
    user_alice = user_dao.get_by_username("aliceasm")
    missing_user = user_dao.get_by_username("missing user")
    assert user_alice is not None
    assert user_alice.username == "aliceasm"
    assert user_alice.firstname == "Alice"
    assert user_alice.lastname == "Asm"
    assert user_alice.account_type == "Administrator"
    assert missing_user is None

def test_create_user(user_dao):
    ResetDatabase().lancer(True)
    to_be_created_user = User(
        username = "created_user",
        firstname = "Created",
        lastname = "User",
        password = "pwdOfCreatedUser123",
        salt = "saltOfCreatedUser",
        account_type = "Customer"
    )
    created_user = user_dao.create_user(to_be_created_user)
    not_to_be_created_user = None
    not_created_user = user_dao.create_user(not_to_be_created_user)
    assert created_user == True
    assert not_created_user == False



if __name__ == "__main__":
    pytest.main()
