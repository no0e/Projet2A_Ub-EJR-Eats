from pydantic import BaseModel
from typing import List

class Delivery(BaseModel):
    id_delivery: int
    username_driv: str
    duration: int
    stops: List[str]

    @property
    def duration(self) -> int:
        return self.duration

    @duration.setter
    def duration(self, value: int):
        self.duration = value

    @property
    def stops(self) -> List[str]:
        return self.stops

    @stops.setter
    def stops(self, value: List[str]):
        self.stops = value
