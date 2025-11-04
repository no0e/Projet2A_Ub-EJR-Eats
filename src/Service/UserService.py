from src.DAO.UserDAO import UserDAO
from src.Model.User import User
from src.Service.PasswordService import check_password_strength, create_salt, hash_password


class UserService:
    """Class with all Service methods of a user."""

    def __init__(self, user_repo: UserDAO):
        self.user_repo = user_repo

    def create_user(self, username: str, firstname: str, lastname: str, password: str, account_type="Customer") -> User:
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
            user's account type, by default "Customer"

        Returns
        -------
        User
            Returns the user that has been created.
        """
        if self._username_exists(username):
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
