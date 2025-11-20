import requests

GOOGLE_API_KEY = "AIzaSyDGimtwk_7rL05kEHAihqXZojrqIsw4AGE"


class GoogleMap:
    def __init__(self, restaurant_location="51 rue Blaise Pascal, 35170 Bruz"):
        self.restaurant_location = restaurant_location
        self.restaurant_coords = {"lat": 48.050245, "lng": -1.741515}

    def geocoding_address(self, address: str):
        """Convertit une adresse en coordonnées GPS."""
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {"address": address, "key": GOOGLE_API_KEY}
        response = requests.get(url, params=params)
        data = response.json()

        if data["status"] != "OK":
            if data["status"] == "ZERO_RESULTS":
                raise TypeError(f"L’adresse {address} est introuvable")
            else:
                raise Exception(f"Erreur Geocoding: {data['status']}")

        location = data["results"][0]["geometry"]["location"]
        return {"lat": location["lat"], "lng": location["lng"]}

    def get_directions(self, destinations: list[dict], mode: str = "driving"):
        """
        Calcule la distance et la durée totales pour un itinéraire à plusieurs étapes.

        Parameters
        ----------
        destinations : list[dict]
            Liste de coordonnées GPS sous la forme [{"lat": 48.0, "lng": -1.7}, {...}, ...].
            Le dernier élément est la destination finale.
        mode : str
            Mode de transport : "driving", "bicycling" ou "walking".

        Returns
        -------
        dict : Contient la distance totale et la durée totale.
        """
        if not destinations:
            raise ValueError("La liste des destinations ne peut pas être vide.")

        origin = f"{self.restaurant_coords['lat']},{self.restaurant_coords['lng']}"
        destination = f"{destinations[-1]['lat']},{destinations[-1]['lng']}"
        waypoints = "|".join(f"{wp['lat']},{wp['lng']}" for wp in destinations[:-1])

        url = "https://maps.googleapis.com/maps/api/directions/json"
        params = {
            "origin": origin,
            "destination": destination,
            "waypoints": waypoints,
            "mode": mode,
            "key": GOOGLE_API_KEY,
        }

        response = requests.get(url, params=params)
        data = response.json()

        if data["status"] != "OK":
            if data["status"] == "ZERO_RESULTS":
                raise Exception("Aucun itinéraire trouvé")
            else:
                raise Exception(f"Erreur Directions: {data['status']}")

        legs = data["routes"][0]["legs"]
        total_distance = sum(leg["distance"]["value"] for leg in legs) / 1000  # km
        total_duration = sum(leg["duration"]["value"] for leg in legs) / 60  # minutes

        return {
            "distance_km": round(total_distance, 2),
            "duration_min": round(total_duration, 2),
            "mode": mode,
            "stops": len(destinations) - 1,
        }

    def generate_google_maps_link(self, destinations: list[dict]):
        """Génère un lien Google Maps avec plusieurs étapes."""
        if not destinations:
            raise ValueError("La liste des destinations ne peut pas être vide.")

        origin = f"{self.restaurant_coords['lat']},{self.restaurant_coords['lng']}"
        destination = f"{destinations[-1]['lat']},{destinations[-1]['lng']}"
        waypoints = "|".join(f"{wp['lat']},{wp['lng']}" for wp in destinations[:-1])

        return f"https://www.google.com/maps/dir/?api=1&origin={origin}&destination={destination}&waypoints={waypoints}"
