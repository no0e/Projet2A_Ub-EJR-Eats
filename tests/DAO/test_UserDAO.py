from typing import Optional

import pytest

from src.DAO.UserDAO import UserDAO
from src.Model.User import User


class MockDBConnector:
    def sql_query(
        self,
        query: str,
        data: Optional[tuple] = None,
        return_type: str = "one",
    ):
        if query == "SELECT * FROM users WHERE username=%s":
            if not data:
                raise Exception("No username provided")
            username = data[0]
            return {
                "username": username,
                "firstname": "Jean",
                "lastname": "Jak",
                "password": "myHashedPassword",
                "salt": "mySalt",
            }
        return None


def test_get_user_by_username():
    user_dao = UserDAO(MockDBConnector())
    user: Optional[User] = user_dao.get_by_username("janjak")

    assert user is not None
    assert user.username == "janjak"
    assert user.firstname == "Jean"
    assert user.lastname == "Jak"
    assert user.password == "myHashedPassword"
    assert user.salt == "mySalt"


class MockDBConnectorForInsert:
    def sql_query(
        self,
        query: str,
        data: dict,
        return_type: str = "one",
    ):
        if "INSERT INTO users" in query:
            return {
                "username": data["username"],
                "firstname": data["firstname"],
                "lastname": data["lastname"],
                "password": data["password"],
                "salt": data["salt"],
                "account_type": data["account_type"],
            }
        return None


def test_insert_into_db():
    mock_db = MockDBConnectorForInsert()
    user_dao = UserDAO(mock_db)

    username = "newuser"
    firstname = "Alice"
    lastname = "Asm"
    salt = "somesalt"
    hashed_password = "hashedpwd"
    account_type = "Customer"

    new_user = user_dao.insert_into_db(
        username=username,
        firstname=firstname,
        lastname=lastname,
        salt=salt,
        hashed_password=hashed_password,
        account_type=account_type,
    )

    assert new_user is not None
    assert new_user.username == username
    assert new_user.firstname == firstname
    assert new_user.lastname == lastname
    assert new_user.password == hashed_password
    assert new_user.salt == salt
    assert new_user.account_type == account_type


if __name__ == "__main__":
    pytest.main()
