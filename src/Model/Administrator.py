from pydantic import BaseModel


class Administrator(BaseModel):
    username: str
    surname: str
    lastname: str
    account_type: str
    password: str
    salt: str
