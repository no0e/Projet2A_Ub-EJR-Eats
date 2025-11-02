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

        return User(
            username=raw_user["username"],
            firstname=raw_user.get("firstname", ""),
            lastname=raw_user.get("lastname", ""),
            password=raw_user.get("password", ""),
            salt=raw_user.get("salt", ""),
            account_type=raw_user.get("account_type", ""),
        )

    def create_user(self, user: User) -> bool:
        """
        Insert a new user into the database .

        :param user: The User object to insert.
        :return: True if the insertion succeeded , False otherwise.
        """
        raw_created_user = self.db_connector.sql_query(
            """
            INSERT INTO users (id, username, firstname, lastname, password, salt, account_type)
            VALUES (DEFAULT, %(username)s, %(firstname)s, %(lastname)s, %(password)s, %(salt)s, %(account_type)s)
            RETURNING *;
            """,
            {
                "username": user.username,
                "firstname": user.firstname,
                "lastname": user.lastname,
                "password": user.password,
                "salt": user.salt,
                "account_type": user.account_type,
            },
            "one",
        )

        return raw_created_user is not None

    def update_user(self, user: User, new_firstname: str, new_lastname: str, new_password: str) -> bool:
        """
        Update an existing user's firstname, lastname, and password in the database.

        :param user: The User object to update .
        :param new_firstname: New first name.
        :param new_lastname: New last name.
        :param new_password: New password (hashed if needed).
        :return: True if the update succeeded, False otherwise.
        """
        updated_rows = self.db_connector.sql_query(
            """
            UPDATE users
            SET
                firstname = %(firstname)s,
                lastname = %(lastname)s,
                password = %(password)s
            WHERE username = %(username)s
            RETURNING *;
            """,
            {
                "username": user.username,
                "firstname": new_firstname,
                "lastname": new_lastname,
                "password": new_password,
            },
            "one",
        )

        return updated_rows is not None

    def delete_user(self, user: User) -> bool:
        """
        Delete an existing user from the database.

        :param user: The User object to delete.
        :return: True if the deletion succeeded, False otherwise.
        """
        deleted_row = self.db_connector.sql_query(
            """
            DELETE FROM users
            WHERE username = %(username)s
            RETURNING *;
            """,
            {
                "username": user.username,
            },
            "one",
        )

        return deleted_row is not None
