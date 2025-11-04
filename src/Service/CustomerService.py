from src.DAO.ItemDAO import ItemDAO

class CustomerServices():

    def __init__(self):
        self.db_connector = DBConnector()  # connexion PostgreSQL via ton DBConnector
        self.item_dao = ItemDAO(self.db_connector)
    
    def View_menu(self):
        """ See all the item disponible

        Return
        ----
        list
            a list of all the exposed items
        """

        return self.item_dao.find_all_exposed_item()





