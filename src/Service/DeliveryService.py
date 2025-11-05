from src.DAO.DeliveryDAO import DeliveryDAO
from src.Service.GoogleMapService import GoogleMap


class DeliveryService:
    """Service métier pour la gestion des livraisons."""

    def __init__(self, delivery_repo: DeliveryDAO):
        self.delivery_repo = delivery_repo
        self.google_map = GoogleMap()

    def get_available_deliveries(self):
        """Retourne toutes les livraisons non acceptées."""
        deliveries = self.delivery_repo.get_available_deliveries()
        return [delivery.__dict__ for delivery in deliveries]

    def accept_delivery(self, id_delivery: int, username_driver: str):
        """
        Permet à un livreur d'accepter une livraison.
        Met à jour la BDD et renvoie un lien Google Maps vers la destination.
        """
        delivery = self.delivery_repo.get_by_id(id_delivery)
        if not delivery:
            raise ValueError("Delivery not found")
        if delivery.is_accepted:
            raise ValueError("Delivery already accepted")

        self.delivery_repo.set_delivery_accepted(id_delivery, username_driver)

        if not delivery.stops or len(delivery.stops) == 0:
            raise ValueError("No delivery stops found")

        destination_address = delivery.stops[-1]  # final stop
        destination_coords = self.google_map.geocoding_address(destination_address)
        google_maps_link = self.google_map.generate_google_maps_link(destination_coords)

        return {
            "message": "Delivery accepted successfully",
            "delivery_id": id_delivery,
            "google_maps_link": google_maps_link,
        }
