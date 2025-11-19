from typing import List, Optional
import pytest

from src.DAO.DeliveryDAO import DeliveryDAO
from src.DAO.DeliveryDriverDAO import DeliveryDriverDAO
from src.Model.Delivery import Delivery
from src.Model.DeliveryDriver import DeliveryDriver
from src.Model.DeliveryDriver import DeliveryDriver
from src.Service.GoogleMapService import GoogleMap
from src.Service.DeliveryDriverService import DeliveryDriverService


class MockDriverRepo:
    def __init__(self):
        self.drivers = {}

    def create(self, driver):
        self.driver[driver.username] = driver

class MockDeliveryRepo:
    def __init__(self):
        self.deliveries = {}

    def find_by_username(self, username: str) -> Optional[Delivery]:
        return self.deiveries.get(username)

    def get_available_deliveries(self) -> List[Delivery]:
        return [delivery for delivery in self.deliveries.values() if delivery.is_accepted is False]

    def set_delivery_accepted(self, delivery_id, driver_username, duration):
        delivery = self.deliveries.get(delivery_id)
        if delivery is None:
            raise ValueError("Delivery not found")

        if delivery["is_accepted"]:
            raise ValueError("Delivery already accepted")

        delivery["is_accepted"] = True
        delivery["username_delivery_driver"] = driver_username
        delivery["duration"] = duration
        id_order = delivery["id_orders"][-1]

        if id_order not in self.orders:
            raise ValueError("Order not found")

        self.orders[id_order]["username_delivery_driver"] = driver_username

        return True

class MockGoogleRepo:
    def __init__(self):
        self.restaurant_coords = {"lat": 48.111339, "lng": -1.68002}

    def generate_google_maps_link(self, destinations: list[dict]):
        if not destinations:
            raise ValueError("The list of destinations cannot be empty")


        origin = f"{self.restaurant_coords['lat']},{self.restaurant_coords['lng']}"

        destination = f"{destinations[-1]['lat']},{destinations[-1]['lng']}"


        waypoints = "|".join(
            f"{wp['lat']},{wp['lng']}" for wp in destinations[:-1]
        )

        return (
            "https://www.google.com/maps/dir/?api=1"
            f"&origin={origin}"
            f"&destination={destination}"
            f"&waypoints={waypoints}"
        )


@pytest.fixture
def driver_repo():
    repo = MockDriverRepo()

    repo.drivers = {
        'ernesto': DeliveryDriver(username_delivery_driver='ernesto', vehicle= 'car', is_available= False),
        'ernesto1': DeliveryDriver(username_delivery_driver='ernesto1', vehicle= 'foot', is_available= True)
        }

    return repo

@pytest.fixture
def delivery_repo():
    repo = MockDeliveryRepo()

    repo.deliveries = {
        DeliveryDriver(username_delivery_driver='ernesto', duration ='50', id_orders= ARRAY[1, 2], stops= ARRAY['13 Main St.', '4 Salty Spring Av.']),
        DeliveryDriver(username_delivery_driver='ernesto1',duration = '15', id_orders = ARRAY[1], stops= ARRAY['13 Main St.'])
        }

    return repo

@pytest.fixture
def google_repo():
    return MockGoogleRepo()

@pytest.fixture
def deliverydriver_service():
    return DeliveryDriverService(
        driver_repo,
        delivery_repo,
        google_repo
    )