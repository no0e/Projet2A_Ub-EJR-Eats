INSERT INTO project_database.users (username, password, firstname, lastname, salt, account_type) 
VALUES
('aliceasm', 'asm123', 'Alice', 'Asm', 'salt', 'Administrator'),
('bobbia', 'tomato1111', 'Bob', 'Bia', 'salt', 'Customer'),
('charliz', 'chachacha', 'Charles', 'Chic', 'saltysalt', 'Customer'),
('drdavid', '!pwd!mypwd', 'David', 'Douze', 'pepper', 'Customer'),
('ernesto', 'hardpwd123', 'Ernest', 'Eagle', 'no', 'DeliveryDriver'),
('ernesto1', 'hardpwd123', 'Ernest', 'Eagle', 'no', 'DeliveryDriver'),
('fabriccio', 'mysuperpwd', 'Fabrice', 'Fantastic', 'mysalt', 'Administrator');

INSERT INTO project_database.administrators  (username_administrator) 
VALUES
('aliceasm'),
('fabriccio');

INSERT INTO project_database.customers  (username_customer, address) 
VALUES
('bobbia', '13 Main St.'),
('charliz', '4 Salty Spring Av.'),
('drdavid', 'Flat 5, Beverly Hills');

INSERT INTO project_database.delivery_drivers (username_delivery_driver, vehicle, is_available)
VALUES
('ernesto', 'car', False),
('ernesto1', 'foot', True);

INSERT INTO project_database.items (id_item, name_item, price, category, stock, exposed)
VALUES 
(1, 'galette saucisse', 3.2, 'main dish', 102, True),
(2, 'vegetarian galette', 3, 'main dish', 30, True),
(3, 'cola', 2, 'drink', 501, True);

INSERT INTO project_database.orders (id_order, username_customer, username_delivery_driver, address, items)
VALUES 
(1, 'bobbia', 'ernesto1', '13 Main St.', '{"1":10}'::jsonb),
(2, 'bobbia', 'ernesto', '13 Main St.', '{"1":39}'::jsonb),
(3, 'charliz', 'ernesto1', '4 Salty Spring Av.', '{"1":39, "3":2}'::jsonb);

INSERT INTO project_database.deliveries (id_delivery, username_delivery_driver, duration, stops)
VALUES 
(1, 'ernesto', '50', ARRAY['13 Main St.', '4 Salty Spring Av.']),
(2, 'ernesto1', '15', ARRAY['13 Main St.']);