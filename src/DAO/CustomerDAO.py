from src.DAO.UserDAO import UserDAO
from src.Model.Customer import Customer


class CustomerDAO(UserDAO):
    def __init__(self, db_connector):
        super().__init__(db_connector)
        self.db = db_connector

    def create(self, customer: Customer) -> bool:
        raw_created_customer = self.db.sql_query(
            """
            INSERT INTO customers (username_customer, address)
            VALUES (%(username_customer)s, %(address)s)
            RETURNING *;
            """,
            {"username_customer": customer.username, "address": customer.address},
            "one",
        )
        return raw_created_customer is not None

    def find_by_username(self, username: str):
        query = """
            SELECT username, adress
            FROM customers
            WHERE username = %s
        """
        raw = self.db.sql_query(query, [username], return_type="one")
        return Customer(**raw) if raw else None

    def update_customer(self, username: str, address: str) -> bool:
        """
        Update an existing customer's address.

        Parameters
        ---
        username: str
            customer's username
        address: str
            new customer's address we want to set in the database

        Return
        ---
        bool
        """
        updated_rows = self.db_connector.sql_query(
            """
            UPDATE customers
            SET address = %(address)s
            WHERE customer_username = %(username)s
            RETURNING *;
            """,
            {"customer_username": Customer.username, "address": Customer.address},
            "one",
        )

        return updated_rows is not None

    def delete(self, customer: Customer) -> bool:
        self.db.sql_query(
            "DELETE FROM customers WHERE username_customer = %s",
            [customer.username],
        )
        return True
