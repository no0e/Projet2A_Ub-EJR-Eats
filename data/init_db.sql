DROP SCHEMA IF EXISTS project_database CASCADE;
CREATE SCHEMA project_database;

--------------------------------------------------------------
-- user
--------------------------------------------------------------
DROP TABLE IF EXISTS project_database.user CASCADE;
CREATE TABLE users (
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
DROP TABLE IF EXISTS project_database.administrator CASCADE;
CREATE TABLE administrators (
  username_administrator VARCHAR UNIQUE NOT NULL,
  FOREIGN KEY (username_administrator) REFERENCES user(username)
);

--------------------------------------------------------------
-- delivery_driver
--------------------------------------------------------------
DROP TABLE IF EXISTS project_database.delivery_driver CASCADE;
CREATE TABLE delivery_drivers (
    username_delivery_driver TEXT PRIMARY KEY REFERENCES users(username),
    vehicle TEXT,
    is_available BOOLEAN
);
--------------------------------------------------------------
-- customer
--------------------------------------------------------------
DROP TABLE IF EXISTS project_database.customer CASCADE;
CREATE TABLE customers (
  username_customer VARCHAR UNIQUE NOT NULL,
  address VARCHAR,
  FOREIGN KEY (username_customer) REFERENCES user(username)
);

--------------------------------------------------------------
-- delivery
--------------------------------------------------------------
DROP TABLE IF EXISTS project_database.delivery CASCADE;
CREATE TABLE deliveries (
  id_delivery INTEGER UNIQUE NOT NULL PRIMARY KEY,
  username_delivery_driver VARCHAR,
  duration INTEGER,
  stops VARCHAR[],
  is_accepted BOOLEAN,
  FOREIGN KEY (username_delivery_driver) REFERENCES user(username)
);

--------------------------------------------------------------
-- item
--------------------------------------------------------------
DROP TABLE IF EXISTS project_database.item CASCADE;
CREATE TABLE items (
  id_item INTEGER UNIQUE NOT NULL PRIMARY KEY,
  name_item VARCHAR,
  price FLOAT,
  category VARCHAR,
  stock INTEGER,
  exposed BOOLEAN
);

--------------------------------------------------------------
-- order_table
--------------------------------------------------------------
DROP TABLE IF EXISTS project_database.order_table CASCADE;
CREATE TABLE orders (
  id_order INTEGER UNIQUE NOT NULL PRIMARY KEY,
  username_customer VARCHAR,
  username_delivery_driver VARCHAR,
  address VARCHAR,
  items item[],
  date_order DATE,
  time_order TIME,
  FOREIGN KEY (username_customer) REFERENCES user(username),
  FOREIGN KEY (username_delivery_driver) REFERENCES user(username)
);
