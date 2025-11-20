from faker import Faker
import random
import json

from src.DAO.DBConnector import DBConnector
from src.Service.PasswordService import hash_password, create_salt

fake = Faker()


def populate_db(n_admins, n_drivers, n_customers, n_items, n_orders, n_deliveries):
    db = DBConnector()

   
    def insert_user(account_type):
        username = fake.unique.user_name()
        raw_pw = fake.password()
        salt = create_salt()
        hashed_pw = hash_password(raw_pw, salt)

        db.sql_query("""
            INSERT INTO project_test_database.users (username, firstname, lastname, password, salt, account_type)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (
            username,
            fake.first_name(),
            fake.last_name(),
            hashed_pw,
            salt,
            account_type
        ))
        return username

   
    admins = []
    drivers = []
    customers = []

    for _ in range(n_admins):
        u = insert_user("ADMIN")
        admins.append(u)
        db.sql_query("""
            INSERT INTO project_test_database.administrators (username_administrator)
            VALUES (%s)
        """, (u,))

    for _ in range(n_drivers):
        u = insert_user("DRIVER")
        drivers.append(u)
        db.sql_query("""
            INSERT INTO project_test_database.delivery_drivers (username_delivery_driver, vehicle, is_available)
            VALUES (%s,%s,%s)
        """, (
            u,
            random.choice(["driving", "bicycling", "walking"]),
            fake.boolean()
        ))

    for _ in range(n_customers):
        u = insert_user("CUSTOMER")
        customers.append(u)
        db.sql_query("""
            INSERT INTO project_test_database.customers (username_customer, address)
            VALUES (%s,%s)
        """, (u, fake.address().replace("\n", ", ")))

    # ------------------------------------------------------------
    # ITEMS
    # ------------------------------------------------------------
    item_ids = []
    for _ in range(n_items):
        row = db.sql_query("""
            INSERT INTO project_test_database.items
            (name_item, price, category, stock, exposed)
            VALUES (%s,%s,%s,%s,%s)
            RETURNING id_item
        """, (
            fake.word().capitalize(),
            round(random.uniform(1, 100), 2),
            random.choice(["starter", "main course", "dessert", "drink"]),
            random.randint(0, 200),
            fake.boolean()
        ), return_type="one")
        item_ids.append(row["id_item"])

    # ------------------------------------------------------------
    # ORDERS
    # ------------------------------------------------------------
    order_ids = []
    for _ in range(n_orders):
        items_json = [
            {"id": random.choice(item_ids), "qty": random.randint(1, 4)}
            for _ in range(random.randint(1, 6))
        ]

        row = db.sql_query("""
            INSERT INTO project_test_database.orders
            (username_customer, username_delivery_driver, address, items, date_order, time_order)
            VALUES (%s,%s,%s,%s,%s,%s)
            RETURNING id_order
        """, (
            random.choice(customers),
            random.choice(drivers),
            fake.address().replace("\n", ", "),
            json.dumps(items_json),
            fake.date_between(start_date="-30d", end_date="today"),
            fake.time()
        ), return_type="one")
        order_ids.append(row["id_order"])

   
    for _ in range(n_deliveries):
        nb = random.randint(1, 4)
        selected = random.sample(order_ids, min(nb, len(order_ids)))
        stops = [fake.address().replace("\n", ", ") for _ in selected]

        db.sql_query("""
            INSERT INTO project_test_database.deliveries
            (username_delivery_driver, duration, id_orders, stops, is_accepted)
            VALUES (%s,%s,%s::INTEGER[],%s::TEXT[],%s)
        """, (
            random.choice(drivers),
            random.randint(5, 90),
            selected,
            stops,
            fake.boolean()
        ))


populate_db(
    n_admins=3,
    n_drivers=10,
    n_customers=25,
    n_items=40,
    n_orders=80,
    n_deliveries=30
)