from src.DAO.CustomerDAO import CustomerDAO
from src.DAO.DBConnector import DBConnector
from src.DAO.DeliveryDriverDAO import DeliveryDriverDAO
from src.DAO.ItemDAO import ItemDAO
from src.DAO.OrderDAO import OrderDAO
from src.Model.Customer import Customer
from src.Model.Order import Order
from typing import List


class CustomerService:
    def __init__(self):
        self.db_connector = DBConnector()
        self.item_dao = ItemDAO(self.db_connector)
        self.deliverydriver_dao = DeliveryDriverDAO(self.db_connector)
        self.customer_dao = CustomerDAO(self.db_connector)
        self.order_dao = OrderDAO(self.db_connector)
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

    def update_customer(self, username: str, address: str):
        """Function that update the customer's address.

        Parameters
        ----------
        username : str
            customer's username
        address : str
            customer's address

        Returns
        -------
        User
            Returns the customer with updated information.
        """
        self.customer_dao_repo.get_customer(username).address = address
        return self.customer_dao.get_customer(username)

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

    def add_item_cart(self, username, cart, name_items: List[str], quantities : List[int]) ->dict:
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
                cart[item.id_item] = quantity


        price_cart = sum(item.price * cart[item.id_item] for item in items if item.id_item in cart)


        return {
            "price_cart": price_cart,
            "cart": cart
        }

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
                id_item = item.id_item
                if new_number_item > item.stock:
                    raise ValueError("The quantity requested exceeds the stock available.")
                if item.id_item not in cart:
                    raise TypeError(f"{name_item} is not in the cart")
                cart[id_item] = new_number_item
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
                id_item = item.id_item
                if item.id_item not in cart:
                    raise TypeError(f"{name_item} is not in the cart")
                del cart[id_item]
                return cart

    def validate_cart(self, cart, username_customer, validate, adress):
        customer = self.customer_dao.get_by_username(username_customer)
        if validate.lower() == "yes":
            if adress is None:
                adress = customer.adress
            order = Order(
                id_order=None, username_customer=str, username_delivery_driver=None, address=adress, items=cart
            )
            success = self.order_dao.create_order(order)
            if not success:
                raise ValueError("Failed to create order in the database.")
            return f"You validated your cart, there your {order}"

        raise TypeError("If you want to validate your cart you must enter: yes")
