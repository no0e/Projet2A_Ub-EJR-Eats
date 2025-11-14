from typing import Optional

import pytest

from src.Model.Administrator import Administrator
from src.Model.User import User
from src.Service.AdministratorService import AdministratorService


class MockAdminRepo:
    def __init__(self):
        self.admins = {}

    def create_admin(self, admin: Administrator) -> bool:
        self.admins[admin.username] = admin
        return True


class MockUserRepo:
    def __init__(self):
        self.users = {}

    def create_user(self, user):
        self.users[user.username] = user

    def get_by_username(self, username: str) -> Optional[User]:
        return self.users.get(username)


class MockDriverRepo:
    def __init__(self):
        self.drivers = {}

    def create(self, driver):
        self.drivers[driver.username] = driver


class MockCustomerRepo:
    def __init__(self):
        self.customers = {}

    def create(self, customer):
        self.customers[customer.username] = customer


user_repo = MockUserRepo()
admin_repo = MockAdminRepo()
driver_repo = MockDriverRepo()
customer_repo = MockCustomerRepo()

service = AdministratorService(user_repo, admin_repo, driver_repo, customer_repo)


admin_repo.create_admin(
    Administrator(
        username="janjak",
        firstname="Jean-Jacques",
        lastname="John",
        salt="sodium",
        password="hashed_pass",
        account_type="Customer",
    )
)

user_repo.create_user(User(
    username="Pat",
    firstname="Patric",
    lastname="Pic",
    password="mdpsecured",
    salt= "salt",
    account_type="Customer"
))


def test_create_user_success():
    user = service.create_user("janjon", "Jean", "John", "mdpsecure", account_type="Customer")
    assert user.username == "janjon"
    assert user_repo.get_by_username("janjon") is not None
    assert customer_repo.customers["janjon"].firstname == "Jean"

def test_get_user_success():
    administrator = service.get_user("Pat")
    assert administrator.username == "Pat"
    assert administrator.firstname == "Patric"
    assert administrator.lastname == "Pic"
    assert administrator.password == "mdpsecured"
    assert administrator.salt == "salt"
    assert administrator.account_type == "Customer"

def test_username_exists_success():
    exist = service.username_exists("Pat")
    assert exist is True

def test_username_exists_failed():
    exist = service.username_exists("Jules")
    assert exist is False

def test_delete_user_success():
    user_repo.create_user(User(
        username="Maelys",
        firstname="Mael",
        lastname="Lys",
        password="mdpsecure",
        salt = "salt",
        account_type="Customer"
    ))

    assert service.username_exists("Maelys") is not None
    service.delete_user("Maelys")
    assert user_repo.username_exists("Maelys") is None