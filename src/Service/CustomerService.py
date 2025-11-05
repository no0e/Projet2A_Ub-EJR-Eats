from src.DAO.ItemDAO import ItemDAO
from src.DAO.OrderDAO import OrderDAO
from src.DAO.DeliveryDriverDAO import DeliveryDriverDAO
from src.DAO.CustomerDAO import CustomerDAO
from src.Model.Order import Order
from src.DAO.DBConnector import DBConnector


class CustomerServices():

    def __init__(self):
        self.db_connector = DBConnector()
        self.item_dao = ItemDAO(self.db_connector)
        self.deliverydriver_dao = DeliveryDriverDAO(self.db_connector)
        self.customer_dao = CustomerDAO(self.db_connector)
        self.order_dao = OrderDAO(self.db_connector)

    def View_menu(self):
        """ See all the item disponible

        Return
        ----
        list
            a list of all the exposed items
        """

        return self.item_dao.find_all_exposed_item()


    def add_item_cart(self, cart, name_item : str, number_item : int):
        """ add the quantity of the item choose into the cart

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
        for item in items:
            if item.name_item.lower() == name_item.lower():
                if number_item > item.stock:
                    raise ValueError("The number of {name_item} wanted is not available")
                cart[item.id_item] = cart.get(item.id_item, 0) + number_item
                break
        else:
            raise TypeError("{name_item} was not found among the items proposed")

        price_cart = 0.0
        for item in items:
            if item.id_item in cart:
                price_cart= price_cart + item.price*number_item
        return f"price of the cart{price_cart}, and your cart {cart}"

    def modify_cart(self, cart,  name_item : str, new_number_item : int):
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
            if item.name_item.lower()== name_item.lower():
                id_item = item.id_item
                if new_number_item > item.stock :
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
            if item.name_item.lower()== name_item.lower():
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
                id_order =None,
                username_customer = str,
                username_delivery_driver = None,
                address = adress,
                items= cart
            )
            success = self.order_dao.create_order(order)
            if not success:
                raise ValueError("Failed to create order in the database.")
            return f"You validated your cart, there your {order}"

        raise TypeError ("If you want to validate your cart you must enter: yes")













