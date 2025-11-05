from src.DAO.UserDAO import UserDAO
from src.Model.Administrator import Administrator


class AdministratorDAO(UserDAO):
    def __init__(self, db_connector):
        super().__init__(db_connector)
        self.db = db_connector

    def create(self, administrator: Administrator) -> bool:
        raw_created_admin = self.db.sql_query(
            """
            INSERT INTO administrators (username_administrator)
            VALUES (%(username_administrator)s)
            RETURNING *;
            """,
            {
                "username_administrator": administrator.username,
            },
            "one",
        )
        return raw_created_admin is not None

    def find_by_username(self, username: str):
        query = """
            SELECT u.username, u.firstname, u.lastname, u.password, u.salt, u.account_type
            FROM project_database.users u
            JOIN project_database.administrators a ON u.username = a.username
            WHERE u.username = %s
        """
        raw = self.db.sql_query(query, [username], return_type="one")
        return Administrator(**raw) if raw else None

    def update_administrator(
        self, administrator: Administrator, new_firstname: str, new_lastname: str, new_password: str
    ) -> bool:
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
                "username": Administrator.username,
                "firstname": new_firstname,
                "lastname": new_lastname,
                "password": new_password,
            },
            "one",
        )

        return updated_rows is not None

    def delete(self, administrator: Administrator) -> bool:
        self.db.sql_query(
            "DELETE FROM project_database.administrators WHERE username_administrator = %s",
            [administrator.username],
        )
        return True
