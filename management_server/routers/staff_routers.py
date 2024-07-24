from fastapi import APIRouter
from management_server.schemas import UserSchema
from management_server.controllers import StaffController

router = APIRouter(prefix="/users", tags=["staff"])

@router.get(
    "/staff/{staff_id}",
    response_model=UserSchema,
)
async def get_staff(staff_id):
    staff_controller = StaffController(id=staff_id)
    return  await staff_controller.get()
   


@router.put("/staff/{staff_id}")
async def update_staff(staff_id):
    pass


@router.delete("/staff/{staff_id}")
async def delete_staff(staff_id):
    pass
