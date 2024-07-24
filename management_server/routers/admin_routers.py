from typing import Annotated

from fastapi import APIRouter, Depends, Query
from management_server.controllers import UserController, AdminController
from management_server.schemas import StaffSchema
from management_server.forms import StaffCreateForm, AdminCreateForm

router = APIRouter(prefix="/admin", tags=["staff"])


@router.get(
    "/{admin_id}",
    response_model=StaffSchema,
    response_model_exclude=["updated_at"],
)
async def get_admin(admin_id):
    admin_controller = AdminController(id=admin_id)
    return await admin_controller.get()


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


@router.post(
    "/create-admin/",
    response_model=StaffSchema,
    response_model_exclude=["created_at", "updated_at"],
)
async def create_admin(form_data: Annotated[AdminCreateForm, Depends()]):
    new_admin = await AdminController.create(form_data=form_data.__dict__)
    return new_admin
