from __future__ import annotations
from typing import Dict, ClassVar

from tortoise import fields
from tortoise.models import Model as BaseModel
from management_server.models.helpers import EmailString
from management_server.models.validators import phone_number_vaidator
from management_server.models.helpers import hash_password

class TimestampMixin():
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    modified_at = fields.DatetimeField(null=True, auto_now=True)


class UserModel(TimestampMixin, BaseModel):
    """
    User model class
    """
    user_id = fields.UUIDField(primary_key=True)
    first_name = fields.CharField(max_length=20, min_length=3, null=False)
    last_name = fields.CharField(max_length=20, min_length=3, null=False)
    email = fields.CharField(max_length=100, min_length=10, unique=True, null=False)
    phone_number = fields.CharField(max_length=11, min_length=11, unique=True, null=False)
    mobile_network = fields.CharField(max_length=15, min_length=3, null=False)
    state = fields.CharField(max_length=20, min_length=3, null=False)
    lga = fields.CharField(max_length=20, min_length=3, null=False)
    ward = fields.CharField(max_length=20, min_length=3, null=False)
    password = fields.CharField(max_length=500, null=False)


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
    
    @classmethod
    async def create(cls, **kwargs):
        """
        Create a new instance of the class with the given keyword arguments and save it to the database.

        Args:
            **kwargs: Keyword arguments to initialize the instance.

        Raises:
            ValueError: If the "password" argument is not provided.

        Returns:
            The newly created instance.
        """
        password = kwargs.get("password", None)
        if password is None:
            raise ValueError("Password must be set")
        instance = cls(**kwargs)
        instance.password = hash_password(password)
        await instance.save()
        return instance



class DepartmentModel(BaseModel):
    __tablename__ = "department"
    department_id = fields.UUIDField(primary_key=True)
    name = fields.CharField(max_length=20, min_length=3, null=False, unique=True)
    short_name = fields.CharField(max_length=3, min_length=3, null=False, , unique=True)
    description = fields.TextField(null=False, max_length=255)

    class Meta:
        table = "name"
        ordering = ["name", "short_name"]


class StaffModel(BaseStaffModel, table=True):
    __tablename__ = "staff"
    user_id: ClassVar = Column(String, ForeignKey('user.id'), unique=True, null=False)
    user: UserModel = Relationship(back_populates="staff", sa_relationship_kwargs={"uselist": False, "foreign_keys":[user_id]})
    department_id: ClassVar = Column(String, ForeignKey('department.department_id'), unique=True, null=False)
    department: DepartmentModel = Relationship(
        back_populates="staff_members", sa_relationship_kwargs={"uselist": False, "foreign_keys":[department_id]}
    )
    admin: AdminModel = Relationship(back_populates="staff")


        

class AdminModel(BaseModel, table=True):
    __tablename__ = "admin"
    id: str = fields(default=None, primary_key=True, null=False, index=True)
    staff_id: str = fields(foreign_key="staff.staff_id", null=False, unique=True)
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