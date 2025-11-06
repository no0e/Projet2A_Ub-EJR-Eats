from typing import Optional

from src.DAO.AdministratorDAO import AdministratorDAO
from src.DAO.CustomerDAO import CustomerDAO
from src.DAO.DeliveryDriverDAO import DeliveryDriverDAO
from src.DAO.UserDAO import UserDAO
from src.Model.Administrator import Administrator
from src.Model.Customer import Customer
from src.Model.DeliveryDriver import DeliveryDriver
from src.Model.User import User
from src.Service.PasswordService import check_password_strength, create_salt, hash_password


class UserService:
    """Class with all Service methods of a user."""

    def __init__(
        self,
        user_repo: UserDAO,
        admin_repo: AdministratorDAO,
        driver_repo: DeliveryDriverDAO,
        customer_repo: CustomerDAO,
    ):
        self.user_repo = user_repo
        self.admin_repo = admin_repo
        self.driver_repo = driver_repo
        self.customer_repo = customer_repo

    def create_user(
        self,
        username: str,
        firstname: str,
        lastname: str,
        password: str,
        address="Default address",
        account_type="Customer",
    ) -> User:
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
        address : str
            user's address needed to create a customer account, by default "Default address"
        account_type : str
            user's account type, by default "Customer"


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
        if account_type == "Administrator":
            self.admin_repo.create(
                Administrator(
                    username=username,
                    firstname=firstname,
                    lastname=lastname,
                    password=new_password,
                    salt=salt,
                    account_type=account_type,
                )
            )
        elif account_type == "DeliveryDriver":
            self.driver_repo.create(
                DeliveryDriver(
                    username=username,
                    firstname=firstname,
                    lastname=lastname,
                    password=new_password,
                    salt=salt,
                    account_type=account_type,
                    vehicle="driving",
                    is_available=False,
                )
            )
        else:
            self.customer_repo.create(
                Customer(
                    username=username,
                    firstname=firstname,
                    lastname=lastname,
                    password=new_password,
                    salt=salt,
                    account_type=account_type,
                    address=address,
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
        new_firstname: str
        new_lastname: str
        new_password: str
        if firstname is None:
            new_firstname = self.get_user(username).firstname
        else:
            new_firstname = firstname
        if lastname is None:
            new_lastname = self.get_user(username).lastname
        else:
            new_lastname = lastname
        if password is None:
            new_password = self.get_user(username).password
        else:
            check_password_strength(password)
            salt = create_salt()
            new_password = hash_password(password, salt)
        self.user_repo.update_user(username, new_firstname, new_lastname, new_password)
        return self.user_repo.get_user(username)
