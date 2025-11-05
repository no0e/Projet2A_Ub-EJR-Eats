INSERT INTO users (username, password, firstname, lastname, salt, account_type) 
VALUES
('aliceasm', 'asm123', 'Alice', 'Asm', 'salt', 'Administrator'),
('bobbia', 'tomato1111', 'Bob', 'Bia', 'salt', 'Customer'),
('charliz', 'chachacha', 'Charles', 'Chic', 'saltysalt', 'Customer'),
('drdavid', '!pwd!mypwd', 'David', 'Douze', 'pepper', 'Customer'),
('ernesto', 'hardpwd123', 'Ernest', 'Eagle', 'no', 'DeliveryDriver'),
('ernesto2', 'hardpwd123', 'Ernest', 'Eagle', 'no', 'DeliveryDriver'),
('fabriccio', 'mysuperpwd', 'Fabrice', 'Fantastic', 'mysalt', 'Administrator');

INSERT INTO administrators  (username) 
VALUES
('aliceasm'),
('fabriccio');

INSERT INTO customers  (username, address) 
VALUES
('bobbia', '13 Main St.'),
('charliz', '4 Salty Spring Av.'),
('drdavid', 'Flat 5, Beverly Hills');

INSERT INTO delivery_drivers (username, vehicle, is_available)
VALUES
('ernesto', 'car', False),
('ernesto1', 'foot', True);

INSERT INTO items (id_item, name_item, price, category, stock, exposed)
VALUE (1, 'galette saucisse', 3.2, 'main dish', 102, True),
VALUE (2, 'vegetarian galette', 3, 'main dish', 30, True),
VALUE (3, 'cola', 2, 'drink', 501, True);

INSERT INTO orders (id_order, username_customer, username_delivery_driver, address, items)
VALUE (1, 'bobbia', 'ernesto1', '13 Main St.', {1:10}),
VALUE (2, 'bobbia', 'ernesto', '13 Main St.', {1:39}),
VALUE (3, 'charliz', 'ernesto1', '4 Salty Spring Av.', {1:39, 3:2});

INSERT INTO deliveries (id_delivery, username_driv, duration, stops)
VALUE (1, 'ernesto', '50', ['13 Main St.', '4 Salty Spring Av.']),
VALUE (1, 'ernesto1', '15', ['13 Main St.']);