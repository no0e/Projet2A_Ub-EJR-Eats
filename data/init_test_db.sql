DROP SCHEMA IF EXISTS project_test_database CASCADE;
CREATE SCHEMA project_test_database;

--------------------------------------------------------------
-- user
--------------------------------------------------------------
DROP TABLE IF EXISTS project_test_database.test_users CASCADE;
CREATE TABLE test_users (
    username VARCHAR PRIMARY KEY,
    firstname VARCHAR,
    lastname VARCHAR,
    password VARCHAR,
    salt VARCHAR,
    account_type VARCHAR
);

--------------------------------------------------------------
-- administrator
--------------------------------------------------------------
DROP TABLE IF EXISTS project_test_database.test_administrators CASCADE;
CREATE TABLE teest_administrators (
  username_administrator VARCHAR UNIQUE NOT NULL,
  FOREIGN KEY (username_administrator) REFERENCES users(username)
);

--------------------------------------------------------------
-- delivery_driver
--------------------------------------------------------------
DROP TABLE IF EXISTS project_test_database.test_delivery_drivers CASCADE;
CREATE TABLE test_delivery_drivers (
    username_delivery_driver TEXT PRIMARY KEY REFERENCES users(username),
    vehicle TEXT,
    is_available BOOLEAN
);
--------------------------------------------------------------
-- customer
--------------------------------------------------------------
DROP TABLE IF EXISTS project_test_database.test_customers CASCADE;
CREATE TABLE test_customers (
  username_customer VARCHAR UNIQUE NOT NULL,
  address VARCHAR,
  FOREIGN KEY (username_customer) REFERENCES users(username)
);

--------------------------------------------------------------
-- delivery
--------------------------------------------------------------
DROP TABLE IF EXISTS project_test_database.test_deliveries CASCADE;
CREATE TABLE test_deliveries (
  id_delivery INTEGER UNIQUE NOT NULL PRIMARY KEY,
  username_delivery_driver VARCHAR,
  duration INTEGER,
  stops VARCHAR[],
  is_accepted BOOLEAN,
  FOREIGN KEY (username_delivery_driver) REFERENCES users(username)
);

--------------------------------------------------------------
-- item
--------------------------------------------------------------
DROP TABLE IF EXISTS project_test_database.items CASCADE;
CREATE TABLE test_items (
  id_item SERIAL PRIMARY KEY,
  name_item VARCHAR,
  price FLOAT,
  category VARCHAR,
  stock INTEGER,
  exposed BOOLEAN
);

--------------------------------------------------------------
-- order_table
--------------------------------------------------------------
DROP TABLE IF EXISTS project_test_database.test_orders CASCADE;
CREATE TABLE test_orders (
  id_order INTEGER UNIQUE NOT NULL PRIMARY KEY,
  username_customer VARCHAR,
  username_delivery_driver VARCHAR,
  address VARCHAR,
  items items[],
  date_order DATE,
  time_order TIME,
  FOREIGN KEY (username_customer) REFERENCES users(username),
  FOREIGN KEY (username_delivery_driver) REFERENCES users(username)
);
