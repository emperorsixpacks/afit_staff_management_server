from typing import Annotated
from fastapi import APIRouter, Depends

from management_server.controllers import AuthController
from management_server.forms import LoginForm

router = APIRouter(prefix="/auth")


@router.post("/login", response_model_exclude_none=True)
# @limiter.limit("5/minute")
async def login(
    form_data: Annotated[LoginForm, Depends()],
    # background_tasks: BackgroundTasks, Add a background task to send an email to the user on new login
):
    """
    Login function for authentication.

    :param form_data: Form data containing the login credentials.
    :type form_data: Annotated[LoginForm, Depends()]
    :param request: The request object.
    :type request: Request
    :param response: The response object.
    :type response: Response
    :param background_tasks: The background tasks object.
    :type background_tasks: BackgroundTasks
    :return: Token object containing the authentication token and its expiration time.
    :rtype: Token
    """
    auth_controller = AuthController.model_validate(form_data.__dict__)
    await auth_controller.validate_password()
