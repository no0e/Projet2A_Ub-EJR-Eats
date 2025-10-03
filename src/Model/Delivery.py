from pydantic import BaseModel


class Delivery(BaseModel):
    id_delivery: int
    username_driv: int
    duration: int
    stops: list(str)
