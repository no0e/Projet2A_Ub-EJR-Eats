from typing import Optional

import pytest

from src.Model.User import User
from src.Service.UserService import UserService


class MockUserRepo:
    def get_by_username(self, username: str) -> Optional[User]:
        if username == "janjak":
            return User(
                username="janjak",
                firstname="Jean-Jacques",
                lastname="John",
                salt="jambon",
                password="56d25b0190eb6fcdab76f20550aa3e85a37ee48d520ac70385ae3615deb7d53a",
                account_type="Customer",
            )
        else:
            return None


user_repo = MockUserRepo()


def test_get_user():
    assert UserService(user_repo).get_user("janjak") == User(
        username="janjak",
        firstname="Jean-Jacques",
        lastname="John",
        salt="jambon",
        password="56d25b0190eb6fcdab76f20550aa3e85a37ee48d520ac70385ae3615deb7d53a",
        account_type="Customer",
    )
    assert UserService(user_repo).get_user("janjok") is None


def test_username_exists():
    assert UserService(user_repo)._username_exists("janjak") is True
    assert UserService(user_repo)._username_exists("janjok") is False
