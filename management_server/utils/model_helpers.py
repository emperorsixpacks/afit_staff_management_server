from __future__ import annotations
import os
import json
from random import randint
from typing import List, Dict
from dataclasses import dataclass
from passlib.context import CryptContext

from email_validator import validate_email
from pydantic import EmailStr

from management_server.constants import APP_BASE_URL

MOBILE_PRIFIX_JSON = os.path.join(APP_BASE_URL, "extras/mobile_prefixes.json")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_mobile_prefix() -> List[MobilePrefix]:
    if not os.path.exists(MOBILE_PRIFIX_JSON):
        raise FileNotFoundError(
            f"File: mobile_prefixes.json not found in extras in {APP_BASE_URL}"
        )

    with open(MOBILE_PRIFIX_JSON, "r", encoding="UTF-8") as file:
        data: List[Dict[str, str]] = json.load(file)["mobile"]
        return [
            MobilePrefix(network=network["network"], prefixes=network["prefixes"])
            for network in data
        ]


def hash_password(plain_password: str):
    """
    Hashes a plain password using the bcrypt algorithm.

    Args:
        plain_password (str): The plain password to be hashed.

    Returns:
        str: The hashed password.

    """
    return pwd_context.hash(secret=plain_password)


def generate_staff_id(dept):
    """
    Generate a unique staff ID by combining the department abbreviation and a randomly generated user number.

    Parameters:
        dept (str): The department abbreviation.

    Returns:
        str: The generated staff ID in the format "AFIT{dept}{user_number}".
    """
    user_number = randint(1000, 9999)
    return f"AFIT{dept}{user_number}"


class EmailString(EmailStr):

    @classmethod
    def _validate(cls, input_value: str, /) -> str:
        return validate_email(input_value, check_deliverability=True).email


@dataclass
class MobilePrefix:
    network: str
    prefixes: List[str]
