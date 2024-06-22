from __future__ import annotations
from datetime import datetime
import uuid as uuid_pkg
from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship
from pydantic import ConfigDict

if TYPE_CHECKING:
    from management_server.models import UserModel, AdminModel, DepartmentModel

class BaseModel(SQLModel):
    model_config = ConfigDict(str_strip_whitespace=True, use_enum_values=True, arbitrary_types_allowed=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(
        default_factory=datetime.now
    )  # TODO do not forget to add this when you create the update method

    @property
    def date_created(self):
        """
        Return the date when the user was created.

        :return: The date of creation as a `datetime.date` object.
        """
        return self.created_at.date()

    @property
    def time_created(self):
        """
        Retrieves the time at which the user was created.

        Returns:
            datetime.time: The time at which the object was created.
        """
        return self.created_at.time()


class BaseUserModel(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, use_enum_values=True, arbitrary_types_allowed=True)
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4, primary_key=True
    )


class BaseStaffModel(BaseModel):
    staff_id: str = Field(default=None, primary_key=True, nullable=False, index=True)
    user_id: str = Field(foreign_key="user.id", nullable=False, unique=True)
    user: UserModel = Relationship(back_populates="staff")
    deapartment_head: AdminModel = Relationship(
        back_populates="staff", sa_relationship_kwargs={"uselist": False}
    )
    department_head_id: str = Field(
        foreign_key="admin.staff_id", unique=True, nullable=True
    )
    department_id: str = Field(
        unique=True, nullable=False, foreign_key="department.department_id"
    )
    department: DepartmentModel = Relationship(
        back_populates="staff_members", sa_relationship_kwargs={"uselist": False}
    )
