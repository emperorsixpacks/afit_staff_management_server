from management_server.schemas import UserSchema
from management_server.models import UserModel

def create_new_user(form_data: UserSchema):
    UserModel.create(**form_data)