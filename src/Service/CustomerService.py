from typing import List

from src.DAO.CustomerDAO import CustomerDAO
from src.DAO.DBConnector import DBConnector
from src.DAO.DeliveryDriverDAO import DeliveryDriverDAO
from src.DAO.ItemDAO import ItemDAO
from src.DAO.OrderDAO import OrderDAO
from src.Model.Customer import Customer
from src.Model.Order import Order
from src.Service.DeliveryService import DeliveryService


class CustomerService:
    def __init__(self):
        self.db_connector = DBConnector()
        self.item_dao = ItemDAO(self.db_connector)
        self.deliverydriver_dao = DeliveryDriverDAO(self.db_connector)
        self.customer_dao = CustomerDAO(self.db_connector)
        self.order_dao = OrderDAO(self.db_connector)
        self.delivery_service = DeliveryService(self.db_connector)
        self.active_carts = {}

    def get_customer(self, username: str) -> Customer | None:
        """Function that gives a customer by the username given.

        Parameters
        ----------
        username : str
            customer's username to search

        Returns
        -------
        Customer
            Instance of the customer with the assiociated username given.
        """
        return self.customer_dao.find_by_username(username)

    def view_menu(self):
        """See all the item disponible

        Return
        ----
        menu: list
            a list of all the exposed items
        """
        menu = self.item_dao.find_all_exposed_item()
        return menu

    def get_cart_for_user(self, username: str):
        """Retourne le panier de l'utilisateur associé à son token"""
        return self.active_carts.get(username)

    def add_item_cart(self, username, cart, name_items: List[str], quantities: List[int]) -> dict:
        """add the quantity of the item choose into the cart

        parameters
        -----
        name_item : str
             the name of the item wanted
        number_item : int
            the quantoty wanted

        Returns
        ----
        price_cart : float
            the price of the cart
        """
        items = self.item_dao.find_all_exposed_item()
        items_dict = {item.name_item.lower(): item for item in items}
        for name_item, quantity in zip(name_items, quantities):
            name_item = name_item.lower()
            if name_item not in items_dict:
                raise ValueError(f"Item '{name_item}' not found or not available.")

            item = items_dict[name_item]

            if quantity > item.stock:
                raise ValueError(f"The quantity requested for '{name_item}' exceeds available stock.")

            if item.id_item in cart:
                raise ValueError(f"The item '{name_item}' is already in the cart.")
            else:
                cart[item.name_item] = quantity

        return cart

    def modify_cart(self, cart, name_item: str, new_number_item: int):
        """modify the cart by changing the quatity wanted of an item

        Parameters
        ----
        cart: dict
            the cart of the user
        name_item: str
            name of the item that the user want to update
        new_number_item: int
            the new quantity wanted

        Returns
        -----
        cart: dict
            the new cart
        """
        all_item_available = self.item_dao.find_all_exposed_item()
        for item in all_item_available:
            if item.name_item.lower() == name_item.lower():
                if new_number_item > item.stock:
                    raise ValueError("The quantity requested exceeds the stock available.")
                if name_item.lower() not in [key.lower() for key in cart.keys()]:
                    raise TypeError(f"{name_item} is not in the cart")
                if new_number_item == 0:
                    del cart[item.name_item]
                cart[item.name_item] = new_number_item
                return cart

        raise ValueError(f"Item '{name_item}' not found in the list of items available.")

    def delete_item(self, cart, name_item):
        """Delete an item of the cart

        Parameters
        ----
        cart: dict
            the cart of the user
        name_item: str
            name of the item that the user want to delete


        Returns
        -----
        cart: dict
            the new cart
        """
        all_item_available = self.item_dao.find_all_exposed_item()
        for item in all_item_available:
            if item.name_item.lower() == name_item.lower():
                if item.name_item not in cart:
                    raise TypeError(f"{name_item} is not in the cart")
                del cart[item.name_item]
                return cart

    def validate_cart(self, cart, username_customer, validate, address: str):
        if validate.lower() == "yes":
            order = Order(
                id_order=None,
                username_customer=username_customer,
                username_delivery_driver=None,
                address=address,
                items=cart,
            )
            success = self.order_dao.create_order(order)
            self.delivery_service.create([order])
            if not success:
                raise ValueError("Failed to create order in the database.")
            for name_item, quantity in cart.items():
                items = self.item_dao.find_all_item()
                for item in items:
                    if item.name_item == name_item:
                        id_item = item.id_item
                item = self.item_dao.find_item(id_item)
                if item:
                    if item.stock >= quantity:
                        item.stock -= quantity
                        update_success = self.item_dao.update(item)
                        if not update_success:
                            raise ValueError(f"Failed to update stock for item {item.name_item}")
                    else:
                        raise ValueError(f"Not enough stock for item {item.name_item}")
                else:
                    raise ValueError(f"Item {name_item} not found in the database")

            return f"Your cart has been validated. The order has been created: {order}"

        raise TypeError("If you want to validate your cart you must enter: yes")

    def view_order(self, username_customer: str):
        """See the last order of a customer
        Parameters
        -----
        username_customer: str
            the name of the customer

        Returns
        ------
        order : Order
            the last order of the user
        """
        order_user = self.order_dao.find_order_by_user(username_customer)
        if not order_user:
            raise ValueError(f"No orders found for user {username_customer}")

        last_order = max(order_user, key=lambda order: order.id_order)
        return last_order

    def view_cart(self, cart):
        """See the cart with the price"""
        items = self.item_dao.find_all_item()
        price_cart = sum(item.price * cart[item.name_item] for item in items if item.name_item in cart)

        return {"cart": cart, "price": price_cart}
