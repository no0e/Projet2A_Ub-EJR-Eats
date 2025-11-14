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
    assert user_alice is not None
    assert user_alice.username == "aliceasm"
    assert user_alice.firstname == "Alice"
    assert user_alice.lastname == "Asm"
    assert user_alice.account_type == "Administrator"


if __name__ == "__main__":
    pytest.main()
