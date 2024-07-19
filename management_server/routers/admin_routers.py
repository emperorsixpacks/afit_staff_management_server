from typing import Annotated

from fastapi import APIRouter, Depends
from management_server.controllers import UserController
from management_server.schemas import StaffSchema
from management_server.forms import StaffCreateForm

router = APIRouter(prefix="/users", tags=["staff"])


@router.post(
    "/create-staff",
    response_model=StaffSchema,
    response_model_exclude=["created_at", "updated_at"],
)
async def create_staff(
    form_data: Annotated[StaffCreateForm, Depends()],
):
    new_staff = await UserController.create_new_staff(form_data=form_data)
    return new_staff
