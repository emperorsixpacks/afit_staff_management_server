from __future__ import annotations
from typing import Dict, ClassVar

from tortoise import fields
from tortoise.models import Model as BaseModel
from management_server.models.helpers import EmailString
from management_server.models.validators import phone_number_vaidator
from management_server.models.helpers import hash_password, generate_staff_id


class TimestampMixin:
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
    phone_number = fields.CharField(
        max_length=11, min_length=11, unique=True, null=False
    )
    mobile_network = fields.CharField(max_length=15, min_length=3, null=False)
    state = fields.CharField(max_length=20, min_length=3, null=False)
    lga = fields.CharField(max_length=20, min_length=3, null=False)
    ward = fields.CharField(max_length=20, min_length=3, null=False)
    password_hash = fields.CharField(max_length=500, null=False)
    staff = fields.OneToOneRelation(model_name="staff", related_name="user")

    class Meta:
        table = "user"
        ordering = ["state", "lga", "ward", "created_at"]

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
        password = kwargs.get("password_hash", None)
        if password is None:
            raise ValueError("Password must be set")
        kwargs.update({"password_hash": hash_password(password)})
        instance = cls(**kwargs)
        await instance.save()
        return instance


class DepartmentModel(TimestampMixin, BaseModel):

    department_id = fields.UUIDField(primary_key=True)
    name = fields.CharField(max_length=20, min_length=3, null=False, unique=True)
    short_name = fields.CharField(max_length=3, min_length=3, null=False, unique=True)
    description = fields.TextField(null=False, max_length=255)
    department_head = fields.ForeignKeyField(model_name="admin", on_delete=fields.SET_NULL, null=True)

    class Meta:
        table = "name"
        ordering = ["name", "short_name"]


class StaffModel(TimestampMixin, BaseModel):
    staff_id = fields.CharField(max_length=13, primary_key=True)
    user = fields.OneToOneField(model_name="user", related_name="staff")
    admin = fields.OneToOneNullableRelation(model_name="admin", related_name="staff")
    department_head = fields.ForeignKeyField(
        model_name="admin", on_delete=fields.NO_ACTION
    )
    department = fields.ForeignKeyField(model_name="department", on_delete=fields.SET_NULL, null=True)

    class Meta:
        table = "staff"
        ordering = ["staff_id"]

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
        department: DepartmentModel = kwargs.get("department", None)
        if department is None:
            raise ValueError("Department must be set")
        department_short_name = await DepartmentModel.get(department_id=department.department_id).short_name
        generated_staff_id = generate_staff_id(department_short_name)
        kwargs.update(("staff_id", generated_staff_id))
        instance = cls(**kwargs)
        await instance.save()
        return instance



class Admin(TimestampMixin, BaseModel):
    id = fields.UUIDField(primary_key=True)
    staff = fields.OneToOneField(model_name="staff", related_name="admin", on_delete=fields.CASCADE)

    class Meta:
        table = "admin"
        ordering = ["name", "short_name"]



# TODO check the create command on the usermodel