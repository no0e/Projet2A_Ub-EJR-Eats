from src.DAO.DeliveryDriverDAO import DeliveryDriverDAO
from src.Model.DeliveryDriver import DeliveryDriver
from src.Service.UserService import UserService

class DeliveryDriverService:
    """Class with all Service methods of a delivery driver."""

    def __init__(self, driver_repo: DeliveryDriverDAO):
        self.driver_repo = driver_repo

    def create_deliverydriver(self, username: str, vehicle: str) -> DeliveryDriver:
        """Function that creates a delivery driver from its attributes.

        Parameters
        ----------
        username : str
            user's username
        vehicle : str
            type of vehicle the delivery driver is using

        Returns
        -------
        DeliveryDriver
            Returns the delivery driver that has been created.
        """
        if self._username_exists(username):
            raise ValueError("Username already taken.")
        check_password_strength(password)
        salt = create_salt()
        new_password = hash_password(password, salt)
        self.user_repo.create_user(
            User(
                username=username,
                firstname=firstname,
                lastname=lastname,
                password=new_password,
                salt=salt,
                account_type=account_type,
            )
        )
        return User(
            username=username,
            firstname=firstname,
            lastname=lastname,
            password=new_password,
            salt=salt,
            account_type=account_type,
        )