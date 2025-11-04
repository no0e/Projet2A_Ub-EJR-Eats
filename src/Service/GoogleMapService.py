import requests

GOOGLE_API_KEY = "AIzaSyDGimtwk_7rL05kEHAihqXZojrqIsw4AGE"


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

    def get_directions(self, destination: dict):
        """ " The function give the distance and duration between the restaurant and the adress of delivery

        Parameters
        ----
        destination:dict
            the value of latitude and longitude of the destination

        Returns
        -----
        A dictionnary with the duration (float) and the distance (float)
        """

        destination_position = f"{destination['lat']},{destination['lng']}"
        restaurant_position = f"{self.restaurant_coords['lat']},{self.restaurant_coords['lng']}"
        url = "https://maps.googleapis.com/maps/api/directions/json"
        params = {"origin": restaurant_position, "destination": destination_position, "key": GOOGLE_API_KEY}

        response = requests.get(url, params=params)
        data = response.json()

        if data["status"] != "OK":
            if data["status"] == "ZERO_RESULTS":
                raise Exception("Tere is no itinary possible")
            else:
                raise Exception(f"Erreur Directions: {data['status']}")

        leg = data["routes"][0]["legs"][0]

        return {
            "distance": leg["distance"]["text"],
            "duration": leg["duration"]["text"],
        }

    def generate_google_maps_link(self, destination: dict):
        """Calculate and give the route for the delivery
        -----

        Parameters
        destination: dict
            the gps coordinates of the adress of delivery
        ------
        Returns:
        a link to the route
        """
        destination_position = f"{destination['lat']},{destination['lng']}"
        restaurant_position = f"{self.restaurant_coords['lat']},{self.restaurant_coords['lng']}"
        return f"https://www.google.com/maps/dir/?api=1&origin={restaurant_position}&destination={destination_position}"
