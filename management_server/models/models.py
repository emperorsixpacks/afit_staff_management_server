from __future__ import annotations
from typing import Dict, ClassVar

from tortoise import fields
from tortoise.models import Model as BaseModel
from management_server.models.helpers import EmailString
from management_server.models.validators import phone_number_vaidator

class TimestampMixin():
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    modified_at = fields.DatetimeField(null=True, auto_now=True)


class UserModel(TimestampMixin, BaseModel):
    """
    User model class
    """
    user_id = fields.UUIDField(primary_key=True)
    first_name = fields.CharField(max_length=20, min_length=3, nullable=False)
    last_name = fields.CharField(max_length=20, min_length=3, nullable=False)
    email = fields.CharField(max_length=100, min_length=10, unique=True, nullable=False)
    phone_number = fields.CharField(max_length=11, min_length=11, unique=True, nullable=False)
    mobile_network = fields.CharField(max_length=15, min_length=3, nullable=False)
    state = fields.CharField(max_length=20, min_length=3, nullable=False)
    lga = fields.CharField(max_length=20, min_length=3, nullable=False)
    ward = fields.CharField(max_length=20, min_length=3, nullable=False)
    password = fields.CharField(max_length=500, nullable=False)


    class Meta:
        table = "user"
        ordering = ["state", "lga", "ward"]

    @property
    def full_name(self):
        """
        Returns the full name of the object.

        Returns:
            str: The full name of the object.
        """
        return f"{self.first_name} {self.last_name}"

    @model_validator(mode="before")
    def vaidate_user_model(self, data: Dict):
        """
        Validates the user model before saving it to the database.

        This function is a model validator that is called before saving the user model to the database.
        It performs the following checks:
        - Checks if the 'phone_number' fields is empty and raises an assertion error if it is.
        - Checks if the 'mobile_network' fields is empty and raises an assertion error if it is.
        - Validates the 'phone_number' fields using the 'phone_number_vaidator' function and assigns the result to the 'validate' variable.
        - If the 'validate' variable is None, it raises an error (TODO).
        - Updates the 'mobile_network' fields in the data dictionary with the value from the 'validate.network' attribute.

        Parameters:
            data (Dict): The data dictionary containing the user model data.

        Returns:
            Dict: The updated data dictionary with the 'mobile_network' fields updated.
        """
        user_phone_number = self.get("phone_numeber", None)
        mobile_network = self.get("mobile_network", None)
        assert user_phone_number is None, "fields phone_numeber is empty"

        assert mobile_network is None, "fields mobile_network is empty"

        validate = phone_number_vaidator(phone_number=user_phone_number)
        if validate is None:
            # TODO raise an error here
            pass
        return data.update(("mobile_network", validate.network))


class DepartmentModel(BaseModel, table=True):
    __tablename__ = "department"
    department_id: str = fields(
        default=None, primary_key=True, nullable=False, index=True
    )
    name: str = fields(max_length=20, min_length=3, nullable=False, unique=True)
    short_name: str = fields(max_length=3, min_length=3, nullable=False, unique=True)
    description: str = fields(max_length=250, min_length=10, nullable=True)
    staff_members: StaffModel = Relationship(back_populates="department")
    department_head_id: str = fields(
        unique=True, nullable=False, foreign_key="admin.staff_id"
    )


class StaffModel(BaseStaffModel, table=True):
    __tablename__ = "staff"
    user_id: ClassVar = Column(String, ForeignKey('user.id'), unique=True, nullable=False)
    user: UserModel = Relationship(back_populates="staff", sa_relationship_kwargs={"uselist": False, "foreign_keys":[user_id]})
    department_id: ClassVar = Column(String, ForeignKey('department.department_id'), unique=True, nullable=False)
    department: DepartmentModel = Relationship(
        back_populates="staff_members", sa_relationship_kwargs={"uselist": False, "foreign_keys":[department_id]}
    )
    admin: AdminModel = Relationship(back_populates="staff")


        

class AdminModel(BaseModel, table=True):
    __tablename__ = "admin"
    id: str = fields(default=None, primary_key=True, nullable=False, index=True)
    staff_id: str = fields(foreign_key="staff.staff_id", nullable=False, unique=True)
    staff: StaffModel = Relationship(
        back_populates="admin",
        sa_relationship_kwargs={"uselist": False},
    )

    @fields_validator("id")
    @classmethod
    def validate_admin_model(cls, value):
        print("hello")
        # self.staff_id = str(generate_staff_id(dept="AFIT"))
        # return self

        return value