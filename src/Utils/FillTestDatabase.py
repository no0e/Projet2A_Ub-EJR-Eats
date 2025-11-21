import json
import random

from faker import Faker
import random
import json
import argparse

from src.DAO.DBConnector import DBConnector
from src.Service.PasswordService import create_salt, hash_password

fake = Faker()

def insert_auto(db, schema, table, data_dict):
    cols = list(data_dict.keys())
    vals = list(data_dict.values())
    col_str = ",".join(cols)
    placeholders = ",".join(["%s"] * len(cols))

    sql = f"""
        INSERT INTO {schema}.{table} ({col_str})
        VALUES ({placeholders})
        RETURNING *
    """
    return db.sql_query(sql, vals, return_type="one")


def populate_db(n_admins, n_drivers, n_customers, n_items, n_orders, n_deliveries, database):

    if not database.isidentifier():
        raise ValueError("Invalid schema/database name")

    db = DBConnector()


    print("start users")

    def insert_user(account_type):
        username = fake.unique.user_name()
        salt = create_salt()
        hashed_pw = hash_password(raw_pw, salt)

        db.sql_query(
            """
            INSERT INTO project_test_database.users (username, firstname, lastname, password, salt, account_type)
            VALUES (%s,%s,%s,%s,%s,%s)
        """,
            (username, fake.first_name(), fake.last_name(), hashed_pw, salt, account_type),
        )
        return username

    admins = []
    drivers = []
    customers = []

    for _ in range(n_admins):
        hashed_pw = hash_password(fake.password(), salt)
        return insert_auto(db, database, "users", {
            "username": username,
            "firstname": fake.first_name(),
            "lastname": fake.last_name(),
            "password": hashed_pw,
            "salt": salt,
            "account_type": account_type
        })["username"]

    admins, drivers, customers = [], [], []

    print("admins")
    for i in range(n_admins):
        if i % (n_admins/5) == 0:
            print("admin", i, "/", n_admins)
        u = insert_user("ADMIN")
        admins.append(u)
        db.sql_query(
            """
            INSERT INTO project_test_database.administrators (username_administrator)
            VALUES (%s)
        """,
            (u,),
        )
        insert_auto(db, database, "administrators", {"username_administrator": u})

    print("drivers")
    for i in range(n_drivers):
        if i % (n_drivers/5) == 0:
            print("driver", i, "/", n_drivers)
        u = insert_user("DRIVER")
        drivers.append(u)
        insert_auto(db, database, "delivery_drivers", {
            "username_delivery_driver": u,
            "vehicle": random.choice(["driving", "bicycling", "walking"]),
            "is_available": fake.boolean()
        })

    print("customers")
    for i in range(n_customers):
        if i % (n_customers/5) == 0:
            print("customer", i, "/", n_customers)
        u = insert_user("CUSTOMER")
        customers.append(u)
        db.sql_query(
            """
            INSERT INTO project_test_database.customers (username_customer, address)
            VALUES (%s,%s)
        """,
            (u, fake.address().replace("\n", ", ")),
        )

        insert_auto(db, database, "customers", {
            "username_customer": u,
            "address": fake.address().replace("\n", ", ")
        })

    print("items")
    item_ids = []
    for i in range(n_items):
        if i % (n_items/5) == 0:
            print("item", i, "/", n_items)
        row = insert_auto(db, database, "items", {
            "name_item": fake.word().capitalize(),
            "price": round(random.uniform(1, 100), 2),
            "category": random.choice(["starter", "main course", "dessert", "drink"]),
            "stock": random.randint(0, 200),
            "exposed": fake.boolean()
        })
        item_ids.append(row["id_item"])


    print("orders")
    order_ids = []
    for _ in range(n_orders):
        items_json = [{"id": random.choice(item_ids), "qty": random.randint(1, 4)} for _ in range(random.randint(1, 6))]

        row = db.sql_query(
            """
            INSERT INTO project_test_database.orders
            (username_customer, username_delivery_driver, address, items, date_order, time_order)
            VALUES (%s,%s,%s,%s,%s,%s)
            RETURNING id_order
        """,
            (
                random.choice(customers),
                random.choice(drivers),
                fake.address().replace("\n", ", "),
                json.dumps(items_json),
                fake.date_between(start_date="-30d", end_date="today"),
                fake.time(),
            ),
            return_type="one",
        )
        order_ids.append(row["id_order"])

    for _ in range(n_deliveries):

    print("deliveries")
    for i in range(n_deliveries):
        if i % (n_deliveries/5) == 0:
            print("delivery", i, "/", n_deliveries)
        nb = random.randint(1, 4)
        selected = random.sample(order_ids, min(nb, len(order_ids)))
        stops = [fake.address().replace("\n", ", ") for _ in selected]

        db.sql_query(
            """
            INSERT INTO project_test_database.deliveries
            (username_delivery_driver, duration, id_orders, stops, is_accepted)
            VALUES (%s,%s,%s::INTEGER[],%s::TEXT[],%s)
        """,
            (random.choice(drivers), random.randint(5, 90), selected, stops, fake.boolean()),
        )


    populate_db(
        n_admins=30,
        n_drivers=100,
        n_customers=250,
        n_items=400,
        n_orders=800,
        n_deliveries=300,
        database=database_name
    )