INSERT INTO users (username, password, firstname, lastname, salt, account_type) 
VALUES
("aliceasm", "asm123", "Alice", "Asm", "salt", "Administrator"),
("bobbia", "tomato1111", "Bob", "Bia", "salt", "Customer"),
("charliz", "chachacha", "Charles", "Chic", "saltysalt", "Customer"),
("drdavid", "!pwd!mypwd", "David", "Douze", "pepper", "Customer"),
("ernesto", "hardpwd123", "Ernest", "Eagle", "no", "DeliveryDriver"),
("ernesto2", "hardpwd123", "Ernest", "Eagle", "no", "DeliveryDriver"),
("fabriccio", "mysuperpwd", "Fabrice", "Fantastic", "mysalt", "Administrator");

INSERT INTO administrators  (username) 
VALUES
("aliceasm"),
("fabriccio");

INSERT INTO customers  (username, address) 
VALUES
("bobbia", "13 Main St."),
("charliz", "4 Salty Spring Av."),
("drdavid", "Flat 5, Beverly Hills");

INSERT INTO delivery_drivers (username, vehicle, is_available)
VALUES
("ernesto", "car", False),
("ernesto1", "foot", True);

INSERT INTO items (name_item, price, category, stock, exposed)
VALUE ("galette saucisse", 3.2, "main dish", 102, True);

INSERT INTO orders (username_customer, username_delivery_driver, )

id_order: Optional[int] = None
    username_customer: str
    username_delivery_driver: str
    address: str
    items: Dict[int, int]
