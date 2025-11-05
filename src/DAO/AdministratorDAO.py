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
            SELECT username
            FROM administrators
            WHERE username = %s
        """
        raw = self.db.sql_query(query, [username], return_type="one")
        return Administrator(**raw) if raw else None

    def delete(self, administrator: Administrator) -> bool:
        self.db.sql_query(
            "DELETE FROM project_database.administrators WHERE username_administrator = %s",
            [administrator.username],
        )
        return True
