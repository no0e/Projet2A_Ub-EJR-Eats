import base64
import hashlib
import secrets
from typing import Optional

from src.DAO.UserDAO import UserDAO
from src.Model.User import User


def hash_password(password: str, salt: Optional[str] = None) -> str:
    # Générer un sel si aucun n'est fourni
    if salt is None:
        salt = base64.b64decode(create_salt())
    else:
        salt = base64.b64decode(salt)

    pwd_hash = hashlib.pbkdf2_hmac(
        "sha256",  # algorithme
        password.encode(),  # mot de passe en bytes
        salt,  # sel
        100_000,  # itérations
    )

    # Encode sel et hash en base64 pour stockage
    salt_b64 = base64.b64encode(salt).decode("utf-8")
    hash_b64 = base64.b64encode(pwd_hash).decode("utf-8")

    # Retourne sous la forme "sel$hash"
    return f"{salt_b64}${hash_b64}"


def create_salt() -> str:
    return secrets.token_hex(128)


def check_password_strength(password: str):
    if len(password) < 8:
        raise Exception("Password length must be at least 8 characters")


def validate_username_password(username: str, password: str, user_repo: UserDAO) -> User:
    user_with_username: Optional[User] = user_repo.get_by_username(username=username)
    if hash_password(password, user_repo.salt) != user_with_username.password:
        return None
    return user_with_username
