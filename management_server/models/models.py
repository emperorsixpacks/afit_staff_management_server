from __future__ import annotations
from typing import TypeVar

from fastapi import status

from tortoise import fields
from tortoise.models import Model
from tortoise.transactions import in_transaction
from tortoise.exceptions import IntegrityError


from management_server.utils import (
    hash_password,
    generate_random_password,
    generate_staff_id,
)
from management_server.exceptions import InvalidRequestError


MODEL = TypeVar("MODEL")


class BaseModel(Model):

    @classmethod
    async def _create(cls, instance: MODEL):
        async with in_transaction() as connection:
            await instance.save(using_db=connection, force_create=True)
            return None


class TimestampMixin:
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    modified_at = fields.DatetimeField(null=True, auto_now=True)


class BaseStaffModel(TimestampMixin, BaseModel):
    staff_id = fields.CharField(max_length=13, primary_key=True)
    user: fields.OneToOneRelation["UserModel"] = fields.OneToOneField(
        model_name="models.UserModel", on_delete=fields.CASCADE
    )

    @classmethod
    async def create(cls,**kwargs) -> MODEL:
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
        department_short_name = await DepartmentModel.get_or_none(
            department_id=department.department_id
        ).short_name
        department_staff_count = (
            await StaffModel.filter(department=department).all().count() + 1
        )
        generated_staff_id = generate_staff_id(
            short_name=department_short_name, count=department_staff_count
        )
        kwargs.update(("staff_id", generated_staff_id))
        instance = cls(**kwargs)
        await cls._create(instance)
        return instance


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
    async def create(cls, using_db, **kwargs) -> MODEL:
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
            password = generate_random_password()
            print(password)
        kwargs.update({"password_hash": hash_password(password)})
        instance = cls(**kwargs)
        try:
            await cls._create(instance=instance)
            return instance
        except IntegrityError as e:
            raise InvalidRequestError(
                detail=f"User with this {e}", status_code=status.HTTP_400_BAD_REQUEST
            ) from e


class DepartmentModel(TimestampMixin, BaseModel):

    department_id = fields.UUIDField(primary_key=True)
    name = fields.CharField(max_length=20, min_length=3, null=False, unique=True)
    short_name = fields.CharField(max_length=3, min_length=3, null=False, unique=True)
    description = fields.TextField(null=False, max_length=255)
    department_head: fields.OneToOneNullableRelation["AdminModel"] = (
        fields.OneToOneField(
            model_name="models.AdminModel", on_delete=fields.SET_NULL, null=True
        )
    )

    class Meta:
        table = "department"
        ordering = ["name", "short_name"]


class StaffModel(BaseStaffModel):
    department: fields.OneToOneRelation["DepartmentModel"] = fields.OneToOneField(
        model_name="models.DepartmentModel", on_delete=fields.SET_NULL, null=True
    )

    class Meta:
        table = "staff"
        ordering = ["staff_id"]


class AdminModel(BaseStaffModel):

    class Meta:
        table = "admin"
        ordering = ["id"]
