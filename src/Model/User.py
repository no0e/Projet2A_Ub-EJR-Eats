from pydantic import BaseModel


class User(BaseModel):
    username: str
    surname: str
    lastname: str
    account_type: str
    password: str
    salt: str
