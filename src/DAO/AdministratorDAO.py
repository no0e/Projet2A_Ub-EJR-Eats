from src.DAO.UserDAO import UserDAO
from src.Model.Administrator import Administrator


class AdministratorDAO(UserDAO):
    def __init__(self, db_connector, test: bool = False):
        super().__init__(db_connector, test)

    def create(self, administrator: Administrator) -> bool:
        if not isinstance(administrator, Administrator):
            raise TypeError("The created administrator should be type of administrator.")
        raw_created_admin = self.db_connector.sql_query(
            """
            INSERT INTO """
            + self.schema
            + """.administrators (username_administrator)
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
        if not isinstance(username, str):
            raise TypeError("Username must be a string.")
        if self.get_by_username(username) is None:
            raise ValueError(f"Username {username} does not exist.")
        query = (
            """
            SELECT a.username_administrator as username, u.firstname, u.lastname, u.salt, u.account_type, u.password
            FROM """
            + self.schema
            + """.administrators as a
            JOIN """
            + self.schema
            + """.users as u ON u.username = username
            WHERE username = %s
        """
        )
        raw = self.db_connector.sql_query(query, [username], return_type="one")
        return Administrator(**raw) if raw else None

    def delete(self, administrator: Administrator) -> bool:
        if not isinstance(administrator, Administrator):
            raise TypeError(f"{administrator} should be type of Administrator.")
        if self.find_by_username(administrator.username) is None:
            raise ValueError(f"The administrator {administrator.username} does not exist.")
        self.db_connector.sql_query(
            "DELETE FROM " + self.schema + ".administrators WHERE username_administrator = %s",
            [administrator.username],
        )
        return True
