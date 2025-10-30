import base64
import hashlib
import secrets
from typing import Optional

from src.DAO.UserDAO import UserDAO
from src.Model.User import User


def hash_password(password: str, salt: str) -> str:
    """Function that hash a given password with its salt.

    Parameters
    ----------
    password : str
        raw password
    salt : str
        user's salt

    Returns
    -------
    str
        The hashed password with salt in str type.
    """
    salt = base64.b64decode(salt)
    pwd_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        100_000,
    )
    salt_b64 = base64.b64encode(salt).decode("utf-8")
    hash_b64 = base64.b64encode(pwd_hash).decode("utf-8")
    return f"{salt_b64}${hash_b64}"


def create_salt() -> str:
    """Function that creates a salt

    Returns
    -------
    str
        The salt generated.
    """
    return secrets.token_hex(32)


def check_password_strength(password: str):
    """Function that checks if the password is strong enough.

    Parameters
    ----------
    password : str
        raw password
    """
    if len(password) < 8:
        raise Exception("Password length must be at least 8 characters")


def validate_username_password(username: str, password: str, user_repo: UserDAO) -> User:
    """Function that check if the stored password for a user is the same as when hashed again.

    Parameters
    ----------
    username : str
        username of the user's password we want to check
    password : str
        raw password
    user_repo : UserDAO
        This user's repository with all its stored attributes

    Returns
    -------
    User | None
        It returns the user if the password is the same, None otherwise.
    """
    user_with_username: Optional[User] = user_repo.get_by_username(username)
    if hash_password(password, user_repo.salt) != user_with_username.password:
        return None
    return user_with_username
