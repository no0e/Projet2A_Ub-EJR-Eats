from typing import Optional

from src.DAO.UserRepo import UserRepo
from src.Model.User import User
from src.Service.PasswordService import check_password_strength, create_salt, hash_password


class UserService:
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    def create_user(self, user: User) -> User:
        """"""
        if self._username_exists(user.username):
            raise ValueError("Username already taken.")
        created_user = self.user_repo.insert_into_db(
            user.username, user.firstname, user.lastname, user.salt, user.password
        )
        return User(**created_user)

    def get_user(self, user_username: str) -> User | None:
        """"""
        return self.user_repo.get_by_username(user_username)

    def _username_exists(self, username: str) -> bool:
        """ """
        return self.user_repo.get_by_username(username) is not None
