from typing import Annotated

from fastapi import APIRouter, Request, Depends
from management_server.schemas import UserSchema
from management_server.models import UserModel
from management_server.forms import UserCreateForm
from management_server.controllers import create_new_user

router = APIRouter(prefix="/users", tags=["staff"])


@router.post(
    "/create-staff", response_model=UserSchema, response_model_exclude=["password_hash"]
)
async def create_staff(
    form_data: Annotated[UserCreateForm, Depends()],
    request: Request,
):
    user_info = UserSchema.model_validate(form_data.__dict__)
    await UserModel.create(**user_info.model_dump())
    return user_info


@router.get(
    "/staff/{staff_id}",
    response_model=UserSchema,
    response_model_exclude=["password_hash"],
)
async def get_staff(staff_id):
    pass


@router.put("/staff/{staff_id}")
async def update_staff(staff_id):
    pass


@router.delete("/staff/{staff_id}")
async def delete_staff(staff_id):
    pass
