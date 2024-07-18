"""
Custom Errors used in the application.
"""

from starlette.exceptions import HTTPException


class InvalidRequestError(HTTPException):
    """
    Invalid requests error
    """

    def __init__(
        self, detail: str, status_code: int = 401, headers: dict | None = None
    ) -> None:
        super().__init__(status_code, detail, headers)


class InvalidCredentialsError(HTTPException):
    """
    Credientials error for invalid credentials.
    """

    def __init__(self, detail: str | None = None) -> None:
        self.detail = detail


class ServerFailureError(HTTPException):
    """
    Server failure error
    """

    def __init__(
        self,
        status_code: int = 500,
        detail: str | None = None,
        headers: dict | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)
