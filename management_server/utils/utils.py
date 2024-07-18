import secrets
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_random_password():
    """
    Generate a random password.

    Returns:
        str: The generated random password.
    """
    return secrets.token_hex(16)


def hash_password(plain_password: str):
    """
    Hashes a plain password using the bcrypt algorithm.

    Args:
        plain_password (str): The plain password to be hashed.

    Returns:
        str: The hashed password.

    """
    return pwd_context.hash(secret=plain_password)


def verify_password(hash_pwd, plain_pwd):
    """
    Verify a password by comparing a hashed password with a plain password.

    Args:
        hash_pwd (str): The hashed password to be verified.
        plain_pwd (str): The plain password to be compared with the hashed password.

    Returns:
        bool: True if the plain password matches the hashed password, False otherwise.
    """

    return pwd_context.verify(plain_pwd, hash_pwd)