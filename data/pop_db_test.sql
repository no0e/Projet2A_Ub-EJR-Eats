-- Users
-- password is "hardpwd123" hashed via PasswordService
INSERT INTO project_test_database.users (username, password, firstname, lastname, salt, account_type) 
VALUES
('aliceasm', '364a9f83d2ab94505ba9baecd0fe59c88b082f982e8d8cf8070171bae171fcbe', 'Alice', 'Asm', 'salt', 'Administrator'),
('bobbia', '364a9f83d2ab94505ba9baecd0fe59c88b082f982e8d8cf8070171bae171fcbe', 'Bob', 'Bia', 'salt', 'Customer'),
('charliz', '364a9f83d2ab94505ba9baecd0fe59c88b082f982e8d8cf8070171bae171fcbe', 'Charles', 'Chic', 'saltysalt', 'Customer'),
('drdavid', '364a9f83d2ab94505ba9baecd0fe59c88b082f982e8d8cf8070171bae171fcbe', 'David', 'Douze', 'pepper', 'Customer'),
('ernesto', '364a9f83d2ab94505ba9baecd0fe59c88b082f982e8d8cf8070171bae171fcbe', 'Ernest', 'Eagle', 'no', 'DeliveryDriver'),
('ernesto1', '364a9f83d2ab94505ba9baecd0fe59c88b082f982e8d8cf8070171bae171fcbe', 'Ernest', 'Eagle', 'no', 'DeliveryDriver'),
('fabriccio', '364a9f83d2ab94505ba9baecd0fe59c88b082f982e8d8cf8070171bae171fcbe', 'Fabrice', 'Fantastic', 'mysalt', 'Administrator'),
('futureadministrator', '364a9f83d2ab94505ba9baecd0fe59c88b082f982e8d8cf8070171bae171fcbe', 'Future', 'Administrator', 'salty', 'Administrator'),
('futurecustomer', '364a9f83d2ab94505ba9baecd0fe59c88b082f982e8d8cf8070171bae171fcbe', 'Future', 'Customer', 'salty', 'Customer'),
('futuredeliverydriver', '364a9f83d2ab94505ba9baecd0fe59c88b082f982e8d8cf8070171bae171fcbe', 'Future', 'DeliveryDriver', 'salty', 'DeliveryDriver');

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
('ernesto', 'driving', False),
('ernesto1', 'walking', True);

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
INSERT INTO project_test_database.deliveries (id_delivery, username_delivery_driver, duration, id_orders, stops, is_accepted)
VALUES 
(1,'ernesto', '50', ARRAY[1, 2], ARRAY['13 Main St.', '4 Salty Spring Av.'], True),
(2,'ernesto1', '15', ARRAY[1], ARRAY['13 Main St.'], False);
