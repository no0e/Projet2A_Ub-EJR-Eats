import requests

GOOGLE_API_KEY = "AIzaSyDGimtwk_7rL05kEHAihqXZojrqIsw4AGE"


class GoogleMap:
    def __init__(self, restaurant_location="51 rue Blaise Pascal, 35170 Bruz"):
        self.restaurant_location = restaurant_location
        self.restaurant_coords = {"lat": 48.050245, "lng": -1.741515}

    def geocoding_adress(self, adress: str):
        """Convertit une adresse en coordonnées GPS."""
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {"address": adress, "key": GOOGLE_API_KEY}
        response = requests.get(url, params=params)
        data = response.json()

        if data["status"] != "OK":
            if data["status"] == "ZERO_RESULTS":
                raise TypeError(f"L’adresse {adress} est introuvable")
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

        # Agrégation de toutes les étapes ("legs")
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


class GoogleMap:
    def __init__(self, restaurant_location="51 rue Blaise Pascal, 35170 Bruz"):
        self.restaurant_location = restaurant_location
        self.restaurant_coords = {"lat": 48.050245, "lng": -1.741515}

    def geocoding_adress(self, adress: str):
        """The function is coding the adress. From a written adress it finds GPS coordonates.

        Parameters:
        ------
        adress: str
            the adress given by the customer

        Returns
        -----
        {lat,lng}: dictionary number
            the latitude and longitude of the adress
        """
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {"address": adress, "key": GOOGLE_API_KEY}

        response = requests.get(url, params=params)
        data = response.json()

        if data["status"] != "OK":
            if data["status"] == "ZERO_RESULTS":
                raise TypeError(f"The adress {adress} is not found")
            else:
                raise Exception(f"Erreur Geocoding: {data['status']}")

        location = data["results"][0]["geometry"]["location"]
        return {"lat": location["lat"], "lng": location["lng"]}

    def get_directions(self, destinations: list, mode: str = "driving"):
        """
        Calcule la distance et la durée entre le restaurant et une liste d'arrêts (stops),
        en tenant compte du mode de transport (driving, walking, bicycling).

        Parameters
        ----------
        destinations : list
            Liste de dictionnaires contenant {'lat': float, 'lng': float}
        mode : str
            Type de transport ('driving', 'walking', 'bicycling')

        Returns
        -------
        dict : distance totale et durée totale
        """
        if not destinations:
            raise ValueError("La liste des destinations est vide.")

        origin = f"{self.restaurant_coords['lat']},{self.restaurant_coords['lng']}"
        final_destination = f"{destinations[-1]['lat']},{destinations[-1]['lng']}"
        waypoints = "|".join([f"{d['lat']},{d['lng']}" for d in destinations[:-1]])

        url = "https://maps.googleapis.com/maps/api/directions/json"
        params = {
            "origin": origin,
            "destination": final_destination,
            "waypoints": waypoints,
            "mode": mode,
            "key": GOOGLE_API_KEY,
        }

        response = requests.get(url, params=params)
        data = response.json()

        if data["status"] != "OK":
            raise Exception(f"Erreur Directions: {data['status']}")

        total_distance = 0
        total_duration = 0
        for leg in data["routes"][0]["legs"]:
            total_distance += leg["distance"]["value"]  # en mètres
            total_duration += leg["duration"]["value"]  # en secondes

        return {
            "distance_km": round(total_distance / 1000, 2),
            "duration_min": round(total_duration / 60, 2),
            "mode": mode,
        }

    def generate_google_maps_link(self, destinations: list, mode: str = "driving"):
        """
        Génère un lien Google Maps avec itinéraire comportant plusieurs arrêts.

        Parameters
        ----------
        destinations : list
            Liste de dictionnaires {'lat': float, 'lng': float}
        mode : str
            Type de transport ('driving', 'walking', 'bicycling')

        Returns
        -------
        str
            Lien Google Maps complet pour visualiser l’itinéraire
        """
        if not destinations:
            raise ValueError("La liste des destinations est vide.")

        origin = f"{self.restaurant_coords['lat']},{self.restaurant_coords['lng']}"
        final_destination = f"{destinations[-1]['lat']},{destinations[-1]['lng']}"
        waypoints = "|".join([f"{d['lat']},{d['lng']}" for d in destinations[:-1]])

        url = (
            f"https://www.google.com/maps/dir/?api=1&origin={origin}&destination={final_destination}&travelmode={mode}"
        )

        if waypoints:
            url += f"&waypoints={waypoints}"

        return url


gm = GoogleMap()
destinations = [
    {"lat": 48.051, "lng": -1.741},
    {"lat": 48.07, "lng": -1.74},
    {"lat": 48.08, "lng": -1.72},
]
result = gm.get_directions(destinations, mode="bicycling")
print(result)


link = gm.generate_google_maps_link(destinations, mode="bicycling")
print(link)
