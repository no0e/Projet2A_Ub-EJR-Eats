from typing import List, Optional

import pytest

from src.Model.Delivery import Delivery
from src.Service.DeliveryService import DeliveryService


class MockDeliveryRepo:
    def __init__(self):
        self.deliveries = {}

    def create(self, delivery: Delivery):
        delivery.id_item = self.auto_id
        self.auto_id += 1

        for existing in self.deliveries.values():
            if existing.name_item.lower() == delivery.name_item.lower():
                return False

        self.deliveries[delivery.id_item] = delivery
        return True

    def find_by_username(self, username: str) -> Optional[Delivery]:
        return self.deliveries.get(username)

    def get_available_deliveries(self) -> List[Delivery]:
        return [delivery for delivery in self.deliveries.values() if delivery.is_accepted is False]

    def get_by_id(self, id_delivery) -> Delivery:
        return self.deliveries.get(id_delivery)

    def set_delivery_accepted(self, id_delivery: int, username_delivery_driver: str):
        if id_delivery == 4:
            return False

        delivery = self.deliveries.get(id_delivery)

        if not delivery:
            raise ValueError("Delivery not found")

        if not delivery.id_orders:
            raise ValueError("Orders not found for delivery")

        delivery.is_accepted = True
        delivery.username_delivery_driver = username_delivery_driver
        delivery = self.deliveries.get(id_delivery)

        if not delivery:
            raise ValueError("Delivery not found")

        if not delivery.id_orders:
            raise ValueError("Orders not found for delivery")

        # Simule : is_accepted = TRUE + driver assigné
        delivery.is_accepted = True
        delivery.username_delivery_driver = username_delivery_driver

        # Simule : UPDATE orders SET username_delivery_driver
        last_order_id = delivery.id_orders[-1]
        if str(last_order_id) not in self.orders:
            # crée un mock d'ordre si nécessaire
            self.orders[str(last_order_id)] = {"id_order": last_order_id}

        self.orders[str(last_order_id)]["username_delivery_driver"] = username_delivery_driver

        # Le **service** attend que ce mock retourne aussi *destinations*
        destinations = [
            {
                "lat": 48.117266,  # ex coords → à ajuster si besoin
                "lng": -1.6777926,
                "address": stop,
            }
            for stop in delivery.stops
        ]

        return delivery, destinations

    def accept_delivery(self, delivery_id: int, driver_username: str) -> dict:
        deliveries = self.delivery_repo.get_available_deliveries()
        delivery = next((d for d in deliveries if d.id_delivery == delivery_id), None)
        if not delivery:
            raise ValueError("Delivery not available or already accepted")

        success = self.delivery_repo.set_delivery_accepted(delivery_id, driver_username)
        if not success:
            raise ValueError("Delivery could not be accepted")

        # ----------------------------------------------------------------------
        # CORRECTION : On passe la liste complète des stops au service Google.
        # Le service Google (ou le mock) est responsable de déterminer la destination
        # finale (le dernier stop) et les waypoints (les stops intermédiaires).

        if delivery.stops:
            destinations_for_map = delivery.stops  # Passe ['13 Main St.']
        else:
            # Fallback (doit être cohérent avec ce que le mock attend - ici, un dict unique)
            # MAIS ATTENTION : Si le mock attend une liste (Cas 1 ou 2), il faut encapsuler !
            destinations_for_map = [{"lat": 48.050245, "lng": -1.741515}]

        link = self.google_service.generate_google_maps_link(destinations_for_map)
        # ----------------------------------------------------------------------

        return {"delivery_id": delivery_id, "google_maps_link": link}


class MockGoogleMap:
    """Mock to simulate the Google Maps API."""

    def geocoding_address(self, address: str) -> dict:
        """Simulate the convertion of an address into GPS coordonates."""
        if "Paris" in address:
            return {"lat": 48.8566, "lng": 2.3522}
        if "Lyon" in address:
            return {"lat": 45.7640, "lng": 4.8357}
        if "Unknown address" in address:
            raise TypeError(f"The address is unfoundable")
        return {"lat": 0.0, "lng": 0.0}

    def get_directions(self, destinations: List[dict], mode: str) -> dict:
        """Simulate the calculation of an itinary and a duration."""
        duration = 15 + (len(destinations) * 15)

        return {"duration_min": duration}

    def generate_google_maps_link(self, destination_coords: List[dict]) -> str:
        """Simulate the creation of a Google Maps link."""
        lat = destination_coords[0]["lat"]
        lng = destination_coords[0]["lng"]
        return f"https://mock.google.com/maps?q={lat},{lng}"


@pytest.fixture
@pytest.fixture
def delivery_repo():
    repo = MockDeliveryRepo()

    repo.deliveries = {
        1: Delivery(
            id_delivery=1,
            username_delivery_driver="ernesto",
            duration="50",
            id_orders=[1, 2],
            stops=["13 Main St.", "4 Salty Spring Av."],
            is_accepted=True,
        ),
        2: Delivery(
            id_delivery=2,
            username_delivery_driver="ernesto1",
            duration="15",
            id_orders=[1],
            stops=["13 Main St."],
            is_accepted=False,
        ),
        3: Delivery(
            id_delivery=3,
            username_delivery_driver="driver_test",
            duration="10",
            id_orders=[3],
            stops=[],
            is_accepted=True,
        ),
        4: Delivery(
            id_delivery=4,
            username_delivery_driver=None,
            duration="10",
            id_orders=[3],
            stops=["10 Failed St."],
            is_accepted=False,
        ),
    }
    return repo


@pytest.fixture
def googlemap():
    return MockGoogleMap()


@pytest.fixture
def delivery_service(delivery_repo, googlemap):
    return DeliveryService(delivery_repo, googlemap)


def test_create_success(delivery_service):
    delivery = delivery_service.create([1, 2], ["13 Main St.", "4 Salty Spring Av."])
    assert delivery.id_orders == [1, 2]
    assert delivery.stops == ["13 Main St.", "4 Salty Spring Av."]
