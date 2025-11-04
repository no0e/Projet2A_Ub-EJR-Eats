from src.DAO.ItemDAO import ItemDAO
from src.DAO.OrderDAO import OrderDAO


class CustomerServices():

    def __init__(self):
        self.db_connector = DBConnector()
        self.item_dao = ItemDAO(self.db_connector)

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
        return price_cart

    def validate_cart(self, cart, validate):
        if validate.lower() == "yes":
            order = Order(
                id_order =None
                username_customer = str
                username_delivery_driver = str
                address = str
                items= cart
            )
            create_order(oder)












