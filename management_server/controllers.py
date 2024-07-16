from management_server.schemas import UserSchema
from management_server.models import UserModel

async def create_user_controller(form_data: UserSchema):
    created_user = await UserModel.create(**form_data.model_dump(exclude_unset=True))
    return UserSchema.model_validate(created_user.__dict__)