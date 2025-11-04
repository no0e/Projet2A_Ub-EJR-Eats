from typing import Optional, Union

from src.DAO.AdministratorDAO import AdministratorDAO
from src.DAO.UserDAO import UserDAO
from src.Model.User import User
from src.Model.DeliveryDriver import DeliveryDriver
from src.Service.PasswordService import check_password_strength, create_salt, hash_password


class AdministratorService:
    """Class with all Service methods of a user."""

    def __init__(self, user_repo: UserDAO):
        self.user_repo = user_repo

    def create_user(self, username: str, firstname: str, lastname: str, password: str, account_type: str) -> User:
        """Function that creates a user from its attributes.

        Parameters
        ----------
        username : str
            user's username
        firstname : str
            user's firstname
        lastname : str
            user's lastname
        password : str
            user's password
        account_type : str
            user's account type

        Returns
        -------
        User
            Returns the user that has been created.
        """
        if self.username_exists(username):
            raise ValueError("Username already taken.")
        check_password_strength(password)
        salt = create_salt()
        new_password = hash_password(password, salt)
        self.user_repo.create_user(
            User(
                username=username,
                firstname=firstname,
                lastname=lastname,
                password=new_password,
                salt=salt,
                account_type=account_type,
            )
        )
        return User(
            username=username,
            firstname=firstname,
            lastname=lastname,
            password=new_password,
            salt=salt,
            account_type=account_type,
        )

    def get_user(self, user_username: str) -> User | None:
        """Function that gives a user by the username given.

        Parameters
        ----------
        user_username : str
            user's username to search

        Returns
        -------
        User
            Instance of the user with the assiociated username given.
        """
        return self.user_repo.get_by_username(user_username)

    def username_exists(self, username: str) -> bool:
        """Function that checks if a given username is already existing in the database.

        Parameters
        ----------
        username : str
            username to check

        Returns
        -------
        bool
            True if the username is already existing, False otherwise.
        """
        return self.user_repo.get_by_username(username) is not None

    def delete_user(self, username: str):
        """Function that delete a user from our data given their username.

        Parameters
        ----------
        username : str
            username of the user we want to delete.
        """
        self.user_repo.delete_user(self.get_user(username))

    def update_user(self, username: str, firstname: Optional[str], lastname: Optional[str], password: Optional[str]):
        """Function that update the user's attributes.

        Parameters
        ----------
        username : str
            user's username
        firstname : str | None
            user's firstname
        lastname : str | None
            user's lastname
        password : str | None
            user's password

        Returns
        -------
        User
            Returns the user with updated information.
        """
        if firstname is not None:
            self.user_repo.get_user(username).firstname = firstname
        if lastname is not None:
            self.user_repo.get_user(username).lastname = lastname
        if password is not None:
            check_password_strength(password)
            salt = create_salt()
            self.user_repo.get_user(username).password = hash_password(password, salt)
        return self.user_repo.get_user(username)


    def drivers_available(self) -> list(DeliveryDriver):
        delivery_drivers = self.user_repo.get_by_account_type("DeliveryDriver")
        available_delivery_drivers = [
            delivery_driver
            for delivery_driver in delivery_drivers
            if delivery_driver.is_available
        ]
        return available_delivery_drivers

