from typing import Optional

import pytest

from src.Model.User import User
from src.Service.UserService import UserService


class MockUserRepo:
    def __init__(self):
        self.users = {}

    def create_user(self, user: User) -> bool:
        self.users[user.username] = user

    def get_by_username(self, username: str) -> Optional[User]:
        if username in self.users:
            return self.users[username]
        else:
            return None


user_repo = MockUserRepo()
user_repo.create_user(
    User(
        username="janjak",
        firstname="Jean-Jacques",
        lastname="John",
        salt="jambon",
        password="56d25b0190eb6fcdab76f20550aa3e85a37ee48d520ac70385ae3615deb7d53a",
        account_type="Customer",
    )
)


def test_create_user():
    UserService(user_repo).create_user("janjon", "Jean", "John", "mdpsecure", "Customer")
    assert UserService(user_repo).get_user("janjon") is not None
    with pytest.raises(ValueError) as error_username:
        UserService(user_repo).create_user("janjon", "Jeanette", "Johnny", "mdpsecure2", "Customer")
    assert str(error_username.value) == "Username already taken."
    with pytest.raises(Exception) as exception_password:
        UserService(user_repo).create_user("janjok", "Jeanne", "Johnas", "mdp", "Customer")
    assert str(exception_password.value) == "Password length must be at least 8 characters"


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
