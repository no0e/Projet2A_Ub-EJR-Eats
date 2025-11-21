
import pytest

from src.Service.GoogleMapService import GoogleMap

google_service = GoogleMap()


def test_geocoding_address():
    address = google_service.geocoding_address("51 rue Blaise Pascal, 35170 Bruz")
    assert round(address["lat"], 6) == 48.050886
    assert round(address["lng"], 6) == -1.742031
    with pytest.raises(Exception) as exception:
        google_service.geocoding_address("hdjdhfyej")
    assert str(exception.value) == "L’adresse hdjdhfyej est introuvable"


def test_get_directions():
    dest1 = google_service.geocoding_address("11 Avenue Robert Schuman, 35170 Bruz")
    dest2 = google_service.geocoding_address("6 Rue des Frères Mongolfier, 35170 Bruz")
    itinerary = google_service.get_directions([dest1, dest2], "driving")
    assert itinerary["distance_km"] == 12
    assert itinerary["duration_min"] == 4
    assert itinerary["stops"]
