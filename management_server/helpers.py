import os
from enum import StrEnum


def get_base_url(path):
    return os.path.dirname(os.path.abspath(path=path))


class DBType(StrEnum):
    """
    Database types supported
    """

    SQLITE = "sqlite"
    POSTGRSQL = "postgresql"
    MYSQL = "mysql"

