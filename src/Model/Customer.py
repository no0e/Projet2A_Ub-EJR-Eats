from pydantic import BaseModel


class Customer(BaseModel):
    username: str
    surname: str
    lastname: str
    account_type: str
    password: str
    salt: str
    address: str
