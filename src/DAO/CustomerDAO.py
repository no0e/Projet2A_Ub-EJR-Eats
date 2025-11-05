from src.DAO.UserDAO import UserDAO
from src.Model.Customer import Customer


class CustomerDAO(UserDAO):
    def __init__(self, db_connector):
        super().__init__(db_connector)
        self.db = db_connector

    def create(self, customer: Customer) -> bool:
        try:
            self.db.sql_query(
                """
                INSERT INTO project_database.customers (username_customer)
                VALUES (%s)
                """,
                [customer.username],
            )
            return True
        except Exception as e:
            print(f"[CustomerDAO] Error creating customer: {e}")
            return False

    def find_by_username(self, username: str):
        query = """
            SELECT u.username, u.firstname, u.lastname, u.password, u.salt, u.account_type, c.adress
            FROM project_database.users u
            JOIN project_database.customers c a ON u.username = c.username
            WHERE u.username = %s
        """
        raw = self.db.sql_query(query, [username], return_type="one")
        return Customer(**raw) if raw else None

    def update_customer(self, customer: Customer, new_firstname: str, new_lastname: str, new_password: str) -> bool:
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
                "username": Customer.username,
                "firstname": new_firstname,
                "lastname": new_lastname,
                "password": new_password,
            },
            "one",
        )

        return updated_rows is not None

    def delete(self, customer: Customer) -> bool:
        self.db.sql_query(
            "DELETE FROM project_database.customers WHERE username_customer = %s",
            [customer.username],
        )
        return True
