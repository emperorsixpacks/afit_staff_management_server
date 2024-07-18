from fastapi import APIRouter
from management_server.schemas import UserSchema
from management_server.controllers import UserController

router = APIRouter(prefix="/users", tags=["staff"])

@router.get(
    "/staff/{staff_id}",
    response_model=UserSchema,
)
async def get_staff(staff_id):
    user_controller = UserController(user_id=staff_id)
    user_from_db = await user_controller.get_user()
    return user_from_db


@router.put("/staff/{staff_id}")
async def update_staff(staff_id):
    pass


@router.delete("/staff/{staff_id}")
async def delete_staff(staff_id):
    pass
