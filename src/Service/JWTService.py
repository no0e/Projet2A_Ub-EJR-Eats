import os
import time

import jwt
from jwt.exceptions import ExpiredSignatureError

from src.Model.JWTResponse import JWTResponse


class JwtService:
    """
    Handler for JWT encryption and validation
    """

    def __init__(self, secret: str = "", algorithm: str = "HS256"):
        self.secret = secret if secret else os.environ["JWT_SECRET"]
        self.algorithm = algorithm

    def encode_jwt(self, username: str, account_type: str) -> JWTResponse:
        """
        Creates a token with a 10-minute expiry time containing username and account_type.
        """
        payload = {
            "username": username,
            "account_type": account_type,
            "expiry_timestamp": time.time() + 600,
        }
        token = jwt.encode(payload, self.secret, algorithm=self.algorithm)
        return JWTResponse(access_token=token)

    def decode_jwt(self, token: str) -> dict:
        """
        Decodes a JWT and returns its payload.
        """
        return jwt.decode(token, self.secret, algorithms=[self.algorithm])

    def validate_user_jwt(self, token: str) -> dict:
        """
        Validates the JWT.
        """
        decoded = self.decode_jwt(token)
        if decoded["expiry_timestamp"] < time.time():
            raise ExpiredSignatureError("Expired JWT")
        return decoded


jwt_service = JwtService()
