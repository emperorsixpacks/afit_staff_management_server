from fastapi import Request, Response, status
from fastapi.responses import JSONResponse

from pydantic_core import ValidationError
from management_server.exceptions.excptions import (
    InvalidCredentialsError,
    InvalidRequestError,
    ServerFailureError,
)


def _validation_error_handler(request: Request, exc: ValidationError) -> Response:
    print(exc)

    error = exc.errors()[0]
    response = JSONResponse(
        {
            "message": "Invalid Type",
            "location": f"{error['loc']}",
            "type": f"{error['type']}",
        },
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
    )
    return response


def _invalid_request_error_handler(
    request: Request, exc: InvalidRequestError
) -> Response:
    """
    A function that handles invalid request errors.

    Parameters:
    - request (Request): The request object that caused the error.
    - exc (InvalidRequestError): The InvalidRequestError object.

    Returns:
    - response (Response): The response object with error details.
    """
    response = JSONResponse(
        {"error": f"{exc.detail}"}, status_code=exc.status_code, headers=exc.headers
    )
    return response


def _invalid_credentials_handler(
    request: Request, exc: InvalidCredentialsError
) -> Response:
    """
    Handles the scenario when the user provides invalid credentials.

    Args:
        request (Request): The request object representing the incoming HTTP request.
        exc (InvalidCredentialsError): The exception object representing the invalid credentials error.

    Returns:
        Response: The response object representing the HTTP response with a JSON body containing an error message and status code 401 (Unauthorized). The response also includes the "WWW-Authenticate" header with the value "Bearer".
    """
    response = JSONResponse(
        {
            "error": f"Invalid or expired token {exc.detail if exc.detail is not None else ''} "
        },
        status_code=401,
        # headers={"WWW-Authenticate": "Bearer"},
    )
    return response


def _sever_failed_error_handler(request: Request, exc: ServerFailureError) -> Response:
    """
    A function that handles server failure errors.

    Parameters:
    - request (Request): The request object that caused the error.
    - exc (ServerFailureError): The ServerFailureError object.

    Returns:
    - response (Response): The response object with error details.
    """
    response = JSONResponse(
        {"error": f"{exc.detail}"}, status_code=exc.status_code, headers=exc.headers
    )
    return response
