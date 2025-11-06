INSERT INTO project_test_database.users (username, password, firstname, lastname, salt, account_type) 
VALUES
('aliceasm', 'asm123', 'Alice', 'Asm', 'salt', 'Administrator'),
('bobbia', 'tomato1111', 'Bob', 'Bia', 'salt', 'Customer'),
('charliz', 'chachacha', 'Charles', 'Chic', 'saltysalt', 'Customer'),
('drdavid', '!pwd!mypwd', 'David', 'Douze', 'pepper', 'Customer'),
('ernesto', 'hardpwd123', 'Ernest', 'Eagle', 'no', 'DeliveryDriver'),
('ernesto1', 'hardpwd123', 'Ernest', 'Eagle', 'no', 'DeliveryDriver'),
('fabriccio', 'mysuperpwd', 'Fabrice', 'Fantastic', 'mysalt', 'Administrator');

INSERT INTO project_test_database.administrators  (username_administrator) 
VALUES
('aliceasm'),
('fabriccio');

INSERT INTO project_test_database.customers  (username_customer, address) 
VALUES
('bobbia', '13 Main St.'),
('charliz', '4 Salty Spring Av.'),
('drdavid', 'Flat 5, Beverly Hills');

INSERT INTO project_test_database.delivery_drivers (username_delivery_driver, vehicle, is_available)
VALUES
('ernesto', 'car', False),
('ernesto1', 'foot', True);

INSERT INTO project_test_database.items (name_item, price, category, stock, exposed)
VALUES ('galette saucisse', 3.2, 'main dish', 102, True)
RETURNING id_item;
INSERT INTO project_test_database.items (name_item, price, category, stock, exposed)
VALUES ('vegetarian galette', 3, 'main dish', 30, True)
RETURNING id_item;
INSERT INTO project_test_database.items (name_item, price, category, stock, exposed)
VALUES ('cola', 2, 'drink', 501, True)
RETURNING id_item;

INSERT INTO project_test_database.orders (username_customer, username_delivery_driver, address, items)
VALUES 
('bobbia', 'ernesto1', '13 Main St.', '{"1":10}'::jsonb)
RETURNING id_order;
INSERT INTO project_test_database.orders (username_customer, username_delivery_driver, address, items)
VALUES 
('bobbia', 'ernesto', '13 Main St.', '{"1":39}'::jsonb)
RETURNING id_order;
INSERT INTO project_test_database.orders (username_customer, username_delivery_driver, address, items)
VALUES 
('charliz', 'ernesto1', '4 Salty Spring Av.', '{"1":39, "3":2}'::jsonb)
RETURNING id_order;

INSERT INTO project_test_database.deliveries (username_delivery_driver, duration, stops)
VALUES 
('ernesto', '50', ARRAY['13 Main St.', '4 Salty Spring Av.'])
RETURNING id_delivery;
INSERT INTO project_test_database.deliveries (username_delivery_driver, duration, stops)
VALUES 
('ernesto1', '15', ARRAY['13 Main St.'])
RETURNING id_delivery