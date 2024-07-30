from __future__ import annotations
from typing import TypeVar

from fastapi import status

from tortoise import fields
from tortoise.models import Model
from tortoise.transactions import in_transaction
from tortoise.exceptions import IntegrityError, OperationalError


from management_server.utils import (
    hash_password,
    generate_random_password,
    generate_staff_id,
)
from management_server.exceptions import InvalidRequestError, ServerFailureError


MODEL = TypeVar("MODEL")


class BaseModel(Model):

    @classmethod
    async def _create(cls, instance: MODEL, using_db=None):
        async with in_transaction() as connection:
            db = using_db or connection
            await instance.save(using_db=db, force_create=True)
            return None

    class Meta:
        abstract = True


class TimestampMixin:
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    modified_at = fields.DatetimeField(null=True, auto_now=True)

    class Meta:
        abstract = True


class BaseStaffModel(TimestampMixin, BaseModel):
    id = fields.UUIDField(primary_key=True)
    staff_id = fields.CharField(max_length=13)
    user: fields.OneToOneRelation["UserModel"] = fields.OneToOneField(
        model_name="models.UserModel", on_delete=fields.CASCADE
    )

    @classmethod
    async def create(cls, using_db=None, **kwargs) -> MODEL:
        """
        Create a new instance of the class with the given keyword arguments and save it to the database.

        Args:
            **kwargs: Keyword arguments to initialize the instance.

        Raises:
            ValueError: If the "password" argument is not provided.

        Returns:
            The newly created instance.
        """
        try:
            department_id: DepartmentModel = kwargs.get("department_id", None)
            if department_id is None:
                raise ValueError("Department must be set")
            department = await DepartmentModel.get_or_none(
                department_id=department_id
            )
            department_short_name = department.short_name
            department_staff_count = (
                await StaffModel.filter(department=department).all().count() + 1
            )
            generated_staff_id = generate_staff_id(
                short_name=department_short_name, count=department_staff_count
            )
            kwargs.update({"staff_id":generated_staff_id})
            instance = cls(**kwargs)
            await cls._create(instance, using_db=using_db)
            return instance
        except (AttributeError, OperationalError, IntegrityError) as e:
            print(e)
            raise ServerFailureError(detail="Could not create Staff") from e


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
    async def create(cls, using_db=None, **kwargs) -> MODEL:
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
        kwargs.update({"password_hash": hash_password(password)})
        instance = cls(**kwargs)
        try:
            await cls._create(instance=instance, using_db=using_db)
            return instance
        except IntegrityError as e:
            raise InvalidRequestError(
                detail=f"User with this {e}", status_code=status.HTTP_400_BAD_REQUEST
            ) from e


class DepartmentModel(TimestampMixin, BaseModel):

    department_id = fields.UUIDField(primary_key=True)
    name = fields.CharField(max_length=50, min_length=3, null=False, unique=True)
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
    department: fields.ForeignKeyRelation["DepartmentModel"] = fields.ForeignKeyField(
        model_name="models.DepartmentModel", on_delete=fields.SET_NULL, null=True
    )

    class Meta:
        table = "staff"
        ordering = ["staff_id"]


class AdminModel(BaseStaffModel):

    class Meta:
        table = "admin"
        ordering = ["id"]
