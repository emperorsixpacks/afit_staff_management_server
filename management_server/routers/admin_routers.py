from typing import Annotated

from fastapi import APIRouter, Depends
from management_server.controllers import UserController
from management_server.schemas import StaffSchema
from management_server.forms import StaffCreateForm

router = APIRouter(prefix="/admin", tags=["staff"])


@router.post(
    "/create-staff/",
    response_model=StaffSchema,
    response_model_exclude=["created_at", "updated_at"],
)
async def create_staff(
    form_data: Annotated[StaffCreateForm, Depends()],
):
    new_staff = await UserController.create(form_data=form_data.__dict__)
    return new_staff
