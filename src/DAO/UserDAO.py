from typing import Optional

from src.Model.User import User

from .DBConnector import DBConnector


class UserDAO:
    """
    Data Access Object (DAO) for interacting with the 'users' table in the database.
    Provides methods to retrieve and insert user data.
    """

    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector):
        """
        Initialize the UserDAO with a database connector.

        :param db_connector: Instance of DBConnector used to execute SQL queries.
        """
        self.db_connector = db_connector

    def get_by_username(self, username: str) -> Optional[User]:
        """
        Retrieve a user from the database by their username.

        :param username: The username of the user to retrieve.
        :return: A User object if found, otherwise None.
        """
        raw_user = self.db_connector.sql_query("SELECT * FROM users WHERE username=%s", [username], "one")

        if raw_user is None:
            return None

        # Map database fields to User constructor arguments
        return User(
            username=raw_user["username"],
            firstname=raw_user.get("firstname", ""),
            lastname=raw_user.get("lastname", ""),
            password=raw_user.get("password", ""),
            salt=raw_user.get("salt", ""),
        )

    def insert_into_db(
        self, username: str, firstname: str, lastname: str, salt: str, hashed_password: str, account_type: str
    ) -> User:
        """
        Insert a new user into the database and return a corresponding User object.

        :param username: The username for the new user.
        :param firstname: The user's first name.
        :param lastname: The user's last name.
        :param salt: The salt used for password hashing.
        :param hashed_password: The hashed password.
        :param account_type: The type of account
        :return: A User object representing the newly created user.
        """
        raw_created_user = self.db_connector.sql_query(
            """
            INSERT INTO users (id, username, firstname, lastname, salt, password, account_type)
            VALUES (DEFAULT, %(username)s, %(firstname)s, %(lastname)s, %(salt)s, %(password)s, %(account_type)s)
            RETURNING *;
            """,
            {
                "username": username,
                "firstname": firstname,
                "lastname": lastname,
                "salt": salt,
                "password": hashed_password,
                "account_type": account_type,
            },
            "one",
        )

        # Build and return a User instance from the inserted row
        return User(
            username=raw_created_user["username"],
            firstname=raw_created_user.get("firstname", ""),
            lastname=raw_created_user.get("lastname", ""),
            password=raw_created_user.get("password", ""),
            salt=raw_created_user.get("salt", ""),
        )
