from __future__ import annotations
import os
import json
from typing import List, Dict
from dataclasses import dataclass

from email_validator import validate_email
from pydantic import EmailStr

from management_server.constants import APP_BASE_URL

MOBILE_PRIFIX_JSON = os.path.join("extras/mobile_prefixes.json", APP_BASE_URL)


def get_mobile_prefix() -> List[MobilePrefix]:
    if not os.path.exists(MOBILE_PRIFIX_JSON):
        raise FileNotFoundError(
            f"File: mobile_prefixes.json not found in extras in {APP_BASE_URL}"
        )

    with open(MOBILE_PRIFIX_JSON, "r", encoding="UTF-8") as file:
        data: List[Dict[str, str]] = json.load(file)["mobile"]
        return [
            MobilePrefix(network=network, prefixes=prefixes)
            for network, prefixes in data
        ]


class EmailString(EmailStr):

    @classmethod
    def _validate(cls, input_value: str, /) -> str:
        return validate_email(input_value, check_deliverability=True)[1]


@dataclass
class MobilePrefix:
    network: str
    prefixes: List[str]
