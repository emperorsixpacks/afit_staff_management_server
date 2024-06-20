from enum import StrEnum

class DBType(StrEnum):
    """
    Database types supported
    """

    SQLITE = "sqlite"
    POSTGRSQL = "postgresql"
    MYSQL = "mysql"



