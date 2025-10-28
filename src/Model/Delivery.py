from typing import List

from pydantic import BaseModel


class Delivery(BaseModel):
    id_delivery: int
    username_driv: str
    duration: int
    stops: List[str]

