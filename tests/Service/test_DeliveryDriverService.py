from typing import List, Optional
import pytest

from src.DAO.DeliveryDAO import DeliveryDAO
from src.DAO.DeliveryDriverDAO import DeliveryDriverDAO
from src.Model.Delivery import Delivery
from src.Model.Order import Order
from src.Model.DeliveryDriver import DeliveryDriver
from src.Service.GoogleMapService import GoogleMap
from src.Service.DeliveryDriverService import DeliveryDriverService


class MockDriverRepo:
    def __init__(self):
        self.drivers = {}
        self.orders = {}

    def create(self, driver):
        self.drivers[driver.username] = driver

    def find_by_username(self, username: str) -> Optional[DeliveryDriver]:
        return self.drivers.get(username)

class MockDeliveryRepo:
    def __init__(self):
        self.deliveries = {}

    def find_by_username(self, username: str) -> Optional[Delivery]:
        return self.deliveries.get(username)

    def get_available_deliveries(self) -> List[Delivery]:
        return [delivery for delivery in self.deliveries.values() if delivery.is_accepted is False]

    def set_delivery_accepted(self, id_delivery: int, username_delivery_driver: str):
        delivery =  self.deliveries.get(id_delivery)

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
                "lat": 48.117266,     # ex coords → à ajuster si besoin
                "lng": -1.6777926,
                "address": stop
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

        # ------------------------------------------------------------------
        # CORRECTION ICI: 
        # Si delivery.stops existe, utilisez toute la liste des stops
        # S'il n'y a pas de stops (devrait être impossible avec un mock correct), utilisez la valeur par défaut dans une liste.
        
        stops_to_send = delivery.stops if delivery.stops else [{"lat": 48.050245, "lng": -1.741515}]
        link = self.google_service.generate_google_maps_link(stops_to_send)
       
        return {"delivery_id": delivery_id, "google_maps_link": link}

class MockGoogleRepo:
    def __init__(self):
        self.restaurant_coords = {"lat": 48.111339, "lng": -1.68002}

    def generate_google_maps_link(self, destinations):
        if not destinations:
            raise ValueError("The list of destinations cannot be empty")

        origin = f"{self.restaurant_coords['lat']},{self.restaurant_coords['lng']}"

        # Nouvelle vérification: Si c'est une liste de strings (adresses)
        if isinstance(destinations[0], str): # <-- Ajout de cette condition
            destination = destinations[-1] # L'adresse de destination finale
            waypoints = "|".join(d for d in destinations[:-1])

        # Si le mock reçoit des dicts avec "address"
        elif isinstance(destinations[0], dict) and "address" in destinations[0]:
            destination = destinations[-1]["address"]
            waypoints = "|".join(d["address"] for d in destinations[:-1])

        # Si le mock reçoit des dicts de coordonnées
        else:
            destination = f"{destinations[-1]['lat']},{destinations[-1]['lng']}"
            waypoints = "|".join(f"{d['lat']},{d['lng']}" for d in destinations[:-1])

        return (
            # Correction: Ajout du "?" pour les paramètres et suppression du "0" superflu.
            "http://googleusercontent.com/maps.google.com/?" 
            f"origin={origin}"
            f"&destination={destination}"
            f"&waypoints={waypoints}"
        )


@pytest.fixture
def driver_repo():
    repo = MockDriverRepo()

    repo.drivers = {
        'ernesto': DeliveryDriver(username="ernesto",
            firstname="Ernest",
            lastname="Eagle",
            password="364a9f83d2ab94505ba9baecd0fe59c88b082f982e8d8cf8070171bae171fcbe",
            salt="no",
            account_type="DeliveryDriver",
            vehicle="car",
            is_available=False),
        'ernesto1': DeliveryDriver(username="ernesto1",
            firstname="Ernest",
            lastname="Eagle",
            salt="no",
            account_type="DeliveryDriver",
            password="364a9f83d2ab94505ba9baecd0fe59c88b082f982e8d8cf8070171bae171fcbe",
            vehicle="foot",
            is_available=True)
        }

    return repo

@pytest.fixture
def delivery_repo():
    repo = MockDeliveryRepo()

    repo.deliveries = {
        1 : Delivery(id_delivery = 1, username_delivery_driver='ernesto', duration ='50', id_orders= [1, 2], stops= ['13 Main St.', '4 Salty Spring Av.'], is_accepted = True),
        2 : Delivery(id_delivery = 2, username_delivery_driver='ernesto1',duration = '15', id_orders = [1], stops= ['13 Main St.'], is_accepted = False)
        }
    repo.orders ={
        1 : Order(id_order =None,username_customer= "bobbia",username_delivery_driver= "ernesto1", address="13 Main St.",items= {"galette saucisse": 2, "cola": 1}),
        2 : Order(id_order =None,username_customer= "bobbia",username_delivery_driver= "ernesto",address= "13 Main St.",items= {"galette saucisse": 39})
    }

    return repo

@pytest.fixture
def google_repo():
    return MockGoogleRepo()

@pytest.fixture
def deliverydriver_service(driver_repo, delivery_repo, google_repo):
    return DeliveryDriverService(
        driver_repo=driver_repo,
        delivery_repo=delivery_repo,
        google_service=google_repo
    )

def test_get_driver_success(deliverydriver_service):
    driver = deliverydriver_service.get_driver("ernesto")
    assert driver.username == "ernesto"
    assert driver.vehicle == "car"
    assert driver.firstname== "Ernest"
    assert driver.lastname=="Eagle"
    assert driver.password=="364a9f83d2ab94505ba9baecd0fe59c88b082f982e8d8cf8070171bae171fcbe"
    assert driver.salt=="no"
    assert driver.account_type=="DeliveryDriver"
    assert driver.is_available is False

def test_get_available_deliveries_success(deliverydriver_service):
    deliveries = deliverydriver_service.get_available_deliveries()
    assert len(deliveries) == 1

    d = deliveries[0]

    assert d.id_delivery == 2
    assert d.username_delivery_driver == "ernesto1"
    assert d.duration == 15
    assert d.id_orders == [1]
    assert d.stops == ["13 Main St."]
    assert d.is_accepted is False

def test_accept_delivery_success(deliverydriver_service):
    delivery = deliverydriver_service.accept_delivery(2, "ernesto1")
    expected_link = (
        "http://googleusercontent.com/maps.google.com/?" # Correction ici
        "origin=48.111339,-1.68002"
        "&destination=13 Main St."
        "&waypoints="
    )
    assert delivery == {"delivery_id": 2, "google_maps_link": expected_link} # Correction ici