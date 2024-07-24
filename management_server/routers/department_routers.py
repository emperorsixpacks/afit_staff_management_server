from typing import Annotated

from fastapi import APIRouter, Depends

from management_server.controllers import DepartmentController
from management_server.forms import DepartmentCreateForm

router = APIRouter(prefix="/department")


@router.post("/create/")
async def create(form_data: Annotated[DepartmentCreateForm, Depends()]):
    new_department = await DepartmentController.create(form_data=form_data.__dict__)
    return new_department
