from typing import Annotated

from fastapi import APIRouter, Depends
from management_server.controllers import UserController
from management_server.schemas import UserSchema
from management_server.forms import UserCreateForm
from management_server.controllers import UserController

router = APIRouter(prefix="/users", tags=["staff"])


@router.post(
    "/create-staff",
    response_model=UserSchema,
    response_model_exclude=["created_at", "updated_at"],
)
async def create_staff(
    form_data: Annotated[UserCreateForm, Depends()],
):
    user_info = UserSchema.model_validate(form_data.__dict__)
    await UserController.create_new_user(form_data=user_info)
    return user_info

