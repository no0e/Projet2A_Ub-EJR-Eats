-- Users
INSERT INTO project_test_database.users (username, password, firstname, lastname, salt, account_type) 
VALUES
('aliceasm', 'asm123', 'Alice', 'Asm', 'salt', 'Administrator'),
('bobbia', 'tomato1111', 'Bob', 'Bia', 'salt', 'Customer'),
('charliz', 'chachacha', 'Charles', 'Chic', 'saltysalt', 'Customer'),
('drdavid', '!pwd!mypwd', 'David', 'Douze', 'pepper', 'Customer'),
('ernesto', 'hardpwd123', 'Ernest', 'Eagle', 'no', 'DeliveryDriver'),
('ernesto1', 'hardpwd123', 'Ernest', 'Eagle', 'no', 'DeliveryDriver'),
('fabriccio', 'mysuperpwd', 'Fabrice', 'Fantastic', 'mysalt', 'Administrator'),
('futureadministrator', 'pwd222', 'Future', 'Administrator', 'salty', 'Administrator'),
('futurecustomer', 'pwd222', 'Future', 'Customer', 'salty', 'Customer'),
('futuredeliverydriver', 'pwd222', 'Future', 'DeliveryDriver', 'salty', 'DeliveryDriver');

-- Administrators
INSERT INTO project_test_database.administrators  (username_administrator) 
VALUES
('aliceasm'),
('fabriccio');

-- Customers
INSERT INTO project_test_database.customers  (username_customer, address) 
VALUES
('bobbia', '13 Main St.'),
('charliz', '4 Salty Spring Av.'),
('drdavid', 'Flat 5, Beverly Hills');

-- Delivery drivers
INSERT INTO project_test_database.delivery_drivers (username_delivery_driver, vehicle, is_available)
VALUES
('ernesto', 'car', False),
('ernesto1', 'foot', True);

-- Items
INSERT INTO project_test_database.items (name_item, price, category, stock, exposed)
VALUES 
('galette saucisse', 3.2, 'main dish', 102, True),
('vegetarian galette', 3.0, 'main dish', 30, False),
('cola', 2.0, 'drink', 501, True);

-- Orders with string keys in items (adapted for tests)
INSERT INTO project_test_database.orders (username_customer, username_delivery_driver, address, items)
VALUES 
('bobbia', 'ernesto1', '13 Main St.', '{"galette saucisse":2,"cola":1}'::jsonb),
('bobbia', 'ernesto', '13 Main St.', '{"galette saucisse":39}'::jsonb),
('charliz', 'ernesto1', '4 Salty Spring Av.', '{"galette saucisse":39,"cola":2}'::jsonb);

-- Deliveries
INSERT INTO project_test_database.deliveries (username_delivery_driver, duration, id_orders, stops)
VALUES 
('ernesto', '50', ARRAY[1, 2], ARRAY['13 Main St.', '4 Salty Spring Av.']),
('ernesto1', '15', ARRAY[1], ARRAY['13 Main St.']);
