from typing import List

from src.DAO.DeliveryDAO import DeliveryDAO
from src.Model.Delivery import Delivery
from src.Model.Order import Order
from src.Service.GoogleMapService import GoogleMap

googlemap = GoogleMap(restaurant_location="51 rue Blaise Pascal, 35170 Bruz")


class DeliveryService:
    """Service métier pour la gestion des livraisons."""

    def __init__(self, delivery_repo: DeliveryDAO):
        self.delivery_repo = delivery_repo

    def create(self, id_orders: List[int], stops: List[str]) -> Delivery:
        """Create a new delivery

        Parameters
        -----
        orders: list(Order)
            orders contained in the delivery

        Returns
        -----
        Delivery
            The delivery that has been created
        """
        delivery = Delivery(id_orders = id_orders, stops = stops, is_accepted=False)
        success = self.delivery_repo.create(delivery)
        if not success:
            raise ValueError("Failed to create delivery in the database.")
        return delivery

    def get_available_deliveries(self):
        """Retourne toutes les livraisons non acceptées."""
        # duration = googlemap.get_directions(destinations = list, mode: str = "driving")["duration_min"]
        deliveries = self.delivery_repo.get_available_deliveries()
        return [delivery.__dict__ for delivery in deliveries]

    def accept_delivery(self, id_delivery: int, username_driver: str, vehicle: str):
        """
        Permet à un livreur d'accepter une livraison.
        Met à jour la BDD et renvoie un lien Google Maps vers la destination.
        """
        delivery = self.delivery_repo.get_by_id(id_delivery)
        if not delivery:
            raise ValueError("Delivery not found")
        if delivery.is_accepted:
            raise ValueError("Delivery already accepted")

        duration = googlemap.get_directions(destinations=delivery.stops, mode=vehicle)["duration_min"]
        self.delivery_repo.set_delivery_accepted(id_delivery, username_driver, duration)

        if not delivery.stops or len(delivery.stops) == 0:
            raise ValueError("No delivery stops found")
        if not isinstance(delivery.stops, list):
            raise ValueError("Stops are not under a list format.")

        destination_address = delivery.stops[-1]
        destination_coords = self.google_map.geocoding_address(destination_address)
        google_maps_link = self.google_map.generate_google_maps_link(destination_coords)

        return {
            "message": "Delivery accepted successfully",
            "delivery_id": id_delivery,
            "google_maps_link": google_maps_link,
        }
