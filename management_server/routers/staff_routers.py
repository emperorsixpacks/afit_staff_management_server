from typing import Annotated

from fastapi import APIRouter, Depends
from management_server.schemas import UserSchema
from management_server.controllers import StaffController
from management_server.forms import StaffUpdateForm

router = APIRouter(prefix="/users", tags=["staff"])

@router.get(
    "/staff/{staff_id}",
    response_model=UserSchema,
)
async def get_staff(staff_id):
    staff_controller = StaffController(id=staff_id)
    return  await staff_controller.get()


@router.put("/staff/{staff_id}", response_model_by_alias=UserSchema)
async def update_staff(staff_id, form_data: Annotated[StaffUpdateForm, Depends()] ):
    staff_controller = StaffController(id=staff_id, fields=form_data.__dict__)

    return await staff_controller.update()


@router.delete("/staff/{staff_id}")
async def delete_staff(staff_id):
    pass
