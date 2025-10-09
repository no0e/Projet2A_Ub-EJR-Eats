from pydantic import BaseModel


class Delivery(BaseModel):
    _id_delivery: int
    _username_driv: int
    _duration: int
    _stops: list(str)

    def __init__(self, id_delivery, username_driv, duration, stops):
        self.id_delivery = id_delivery
        self.username_driv = username_driv
        self._duration = duration
        self._stops = stops


    @property
    def duration(self):
        """"""
        return self._duration

    @property
    def stops(self):
        """"""
        return self._stops

    @duration.setter
    def duration(self, value):
        """"""
        self._duration = value

    @stops.setter
    def stops(self, value):
        """"""
        self._stops = value


