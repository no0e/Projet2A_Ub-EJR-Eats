from typing import Optional

import pytest

from src.DAO.UserDAO import UserDAO
from src.Model.User import User


class MockDBConnectorForUser:
    def __init__(self):
        self.users = {}

    def sql_query(self, query: str, data=None, return_type: str = "one"):
        if query.strip().startswith("SELECT"):
            username = data[0]
            user = self.users.get(username)
            if return_type == "one":
                return user
            return list(self.users.values())

        if query.strip().startswith("INSERT"):
            user_data = data
            username = user_data["username"]
            if username in self.users:
                return None
            self.users[username] = user_data
            return user_data

        if query.strip().startswith("UPDATE"):
            username = data["username"]
            user = self.users.get(username)
            if not user:
                return None
            user.update(
                {
                    "firstname": data["firstname"],
                    "lastname": data["lastname"],
                    "password": data["password"],
                }
            )
            return user

        if query.strip().startswith("DELETE"):
            username = data["username"]
            return self.users.pop(username, None)


def test_create_user():
    db = MockDBConnectorForUser()
    dao = UserDAO(db)
    user = User(
        username="jdoe", firstname="John", lastname="Doe", password="pass", salt="salt", account_type="customer"
    )

    result = dao.create_user(user)
    assert result is True
    assert "jdoe" in db.users


def test_update_user():
    db = MockDBConnectorForUser()
    dao = UserDAO(db)
    db.users["jdoe"] = {
        "username": "jdoe",
        "firstname": "John",
        "lastname": "Doe",
        "password": "pass",
        "salt": "salt",
        "account_type": "customer",
    }
    user = User(
        username="jdoe", firstname="John", lastname="Doe", password="pass", salt="salt", account_type="customer"
    )

    result = dao.update_user(user, "Jane", "Smith", "newpass")
    assert result is True
    updated_user = db.users["jdoe"]
    assert updated_user["firstname"] == "Jane"
    assert updated_user["lastname"] == "Smith"
    assert updated_user["password"] == "newpass"


def test_delete_user():
    db = MockDBConnectorForUser()
    dao = UserDAO(db)
    db.users["jdoe"] = {"username": "jdoe"}
    user = User(username="jdoe", firstname="", lastname="", password="", salt="", account_type="")

    result = dao.delete_user(user)
    assert result is True
    assert "jdoe" not in db.users


def test_get_by_username():
    db = MockDBConnectorForUser()
    dao = UserDAO(db)
    db.users["jdoe"] = {
        "username": "jdoe",
        "firstname": "John",
        "lastname": "Doe",
        "password": "pass",
        "salt": "salt",
        "account_type": "customer",
    }

    user = dao.get_by_username("jdoe")
    assert user is not None
    assert user.username == "jdoe"
    assert user.firstname == "John"

    missing_user = dao.get_by_username("unknown")
    assert missing_user is None

if __name__ == "__main__":
    pytest.main()
