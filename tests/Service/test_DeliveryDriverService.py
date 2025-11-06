import pytest

from src.Model.Delivery import Delivery
from src.Model.DeliveryDriver import DeliveryDriver
from src.Service.DeliveryDriverService import DeliveryDriverService


class MockDeliveryRepo:
    def __init__(self):
        self.deliveries = []
        self.accepted = {}

    def find_by_username(self, username):
        if username == "driver1":
            return DeliveryDriver(username="driver1", vehicle="bike", status="available")
        return None

    def get_available_deliveries(self):
        return self.deliveries

    def set_delivery_accepted(self, delivery_id, driver_username):
        if any(d.id_delivery == delivery_id for d in self.deliveries):
            self.accepted[delivery_id] = driver_username
            return True
        return False


class MockGoogleMap:
    def generate_google_maps_link(self, destination):
        return f"https://maps.google.com/?q={destination['lat']},{destination['lng']}"


@pytest.fixture
def setup_service():
    delivery_repo = MockDeliveryRepo()
    google_service = MockGoogleMap()
    service = DeliveryDriverService(None, delivery_repo, google_service)
    return service, delivery_repo


def test_get_driver_found(setup_service):
    service, _ = setup_service
    driver = service.get_driver("driver1")
    assert driver.username == "driver1"
    assert driver.vehicle == "bike"


def test_get_driver_not_found(setup_service):
    service, _ = setup_service
    driver = service.get_driver("unknown")
    assert driver is None


def test_get_available_deliveries(setup_service):
    service, repo = setup_service
    repo.deliveries = [
        Delivery(id_delivery=1, stops=[{"lat": 1.0, "lng": 2.0}]),
        Delivery(id_delivery=2, stops=[{"lat": 3.0, "lng": 4.0}]),
    ]
    available = service.get_available_deliveries()
    assert len(available) == 2
    assert available[0].id_delivery == 1


def test_accept_delivery_success(setup_service):
    service, repo = setup_service
    repo.deliveries = [Delivery(id_delivery=10, stops=[{"lat": 48.85, "lng": 2.35}])]

    result = service.accept_delivery(10, "driver1")

    assert result["delivery_id"] == 10
    assert "https://maps.google.com" in result["google_maps_link"]
    assert repo.accepted[10] == "driver1"


def test_accept_delivery_not_found(setup_service):
    service, repo = setup_service
    repo.deliveries = [Delivery(id_delivery=5, stops=[{"lat": 10, "lng": 20}])]

    with pytest.raises(ValueError, match="Delivery not available or already accepted"):
        service.accept_delivery(99, "driver1")


def test_accept_delivery_fail(setup_service):
    service, repo = setup_service
    repo.deliveries = [Delivery(id_delivery=7, stops=[{"lat": 10, "lng": 20}])]

    # Simule un échec du repo (aucun succès renvoyé)
    repo.set_delivery_accepted = lambda _id, _driver: False

    with pytest.raises(ValueError, match="Delivery could not be accepted"):
        service.accept_delivery(7, "driver1")
