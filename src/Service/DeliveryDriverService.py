from src.DAO.DeliveryDriverDAO import DeliveryDriverDAO
from src.DAO.UserDAO import UserDAO
from src.Model.DeliveryDriver import DeliveryDriver
from src.Model.User import User
from src.Service.UserService import UserService


class DeliveryDriverService:
    """Class with all Service methods of a delivery driver."""

    def __init__(self, driver_repo: DeliveryDriverDAO, user_repo: UserDAO):
        self.driver_repo = driver_repo
        self.user_repo = user_repo

    def create_deliverydriver(
        self, username: str, firstname: str, lastname: str, password: str, vehicle: str
    ) -> DeliveryDriver:
        """Function that creates a delivery driver from its attributes.

        Parameters
        ----------
        username : str
            driver's username
        firstname : str
            driver's firstname
        lastname : str
            driver's lastname
        password : str
            driver's password
        vehicle : str
            type of vehicle the delivery driver is using

        Returns
        -------
        DeliveryDriver
            Returns the delivery driver that has been created.
        """
        self.user_repo.create_user(
            username=username, firstname=firstname, lastname=lastname, password=password, account_type="DeliveryDriver"
        )
        self.driver_repo.create(DeliveryDriver(username=username, vehicle=vehicle, is_available=False))
        return DeliveryDriver(username=username, vehicle=vehicle, is_available=False)

<<<<<<< HEAD
=======
    def update_vehicle(self, vehicle: str):
        """Function that set the vehicle given in argument as the new vehicle of the driver.

        Parameters
        ----------
        vehicle : str
            type of vehicle the delivery driver wants to set
        """
        self.vehicle = vehicle
>>>>>>> b7c69afb5cbb4895a74f4f63493aa917cf88ab48
