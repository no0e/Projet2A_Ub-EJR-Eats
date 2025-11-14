from typing import List, Optional

from src.DAO.DeliveryDAO import DeliveryDAO
from src.DAO.DeliveryDriverDAO import DeliveryDriverDAO
from src.Model.Delivery import Delivery
from src.Model.DeliveryDriver import DeliveryDriver
from src.Service.GoogleMapService import GoogleMap


class DeliveryDriverService:
    def __init__(self, delivery_repo: DeliveryDAO, google_service: GoogleMap):
        self.delivery_repo = delivery_repo
        self.google_service = google_service

    def get_driver(self, username: str) -> DeliveryDriver | None:
        """Function that gives a delivery driver by the username given.

        Parameters
        ----------
        username : str
            driver's username to search

        Returns
        -------
        DeliveryDriver
            Instance of the delivery driver with the assiociated username given.
        """
        return self.delivery_repo.find_by_username(username)

    def get_available_deliveries(self) -> List[Delivery]:
        return self.delivery_repo.get_available_deliveries()

    def accept_delivery(self, delivery_id: int, driver_username: str) -> dict:
        deliveries = self.delivery_repo.get_available_deliveries()
        delivery = next((d for d in deliveries if d.id_delivery == delivery_id), None)
        if not delivery:
            raise ValueError("Delivery not available or already accepted")

        success = self.delivery_repo.set_delivery_accepted(delivery_id, driver_username)
        if not success:
            raise ValueError("Delivery could not be accepted")

        destination = delivery.stops[-1] if delivery.stops else {"lat": 48.050245, "lng": -1.741515}
        link = self.google_service.generate_google_maps_link(destination)
        return {"delivery_id": delivery_id, "google_maps_link": link}
