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


if __name__ == "__main__":
    pytest.main()
