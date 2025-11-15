from typing import List, Optional

import pytest

from src.DAO.DBConnector import DBConnector
from src.DAO.UserDAO import UserDAO
from src.DAO.AdministratorDAO import AdministratorDAO
from src.Model.Administrator import Administrator
from src.Utils.reset_db import ResetDatabase


@pytest.fixture
def db_connector():
    db = DBConnector()
    yield db

@pytest.fixture
def user_dao(db_connector):
    return UserDAO(db_connector, test=True)

@pytest.fixture
def administrator_dao(db_connector):
    return AdministratorDAO(db_connector, test=True)

def test_create(administrator_dao):
    ResetDatabase().lancer(True)
    #TO DO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def test_find_by_username(administrator_dao):
    ResetDatabase().lancer(True)
    found_user = administrator_dao.find_by_username("aliceasm")
    assert found_user is not None
    with pytest.raises(TypeError):
        administrator_dao.find_by_username(1)
    with pytest.raises(ValueError):
        administrator_dao.find_by_username("nonexistent")


def test_delete(administrator_dao):
    ResetDatabase().lancer(True)
    
    with pytest.raises(TypeError):
        administrator_dao.delete(1)
    with pytest.raises(ValueError):
        administrator_dao.delete(
            Administrator(
                username="nonexistentadministrator",
                firstname="nonexistent",
                lastname="administrator",
                password="pwd12345",
                salt="salt",
                account_type="Adlinistrator"
            )
        )



if __name__ == "__main__":
    pytest.main()
    ResetDatabase().lancer(True)
