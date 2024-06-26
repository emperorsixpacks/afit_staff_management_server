from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["staff"])


@router.post("/create-staff")
async def create_staff():
    pass

@router.get("/staff/{staff_id}")
async def get_staff(staff_id):
    pass

@router.put("/staff/{staff_id}")
async def update_staff(staff_id):
    pass

@router.delete("/staff/{staff_id}")
async def delete_staff(staff_id):
    pass