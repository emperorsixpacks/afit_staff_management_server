from __future__ import annotations
from typing import Dict
from random import randint
from pydantic import model_validator


from sqlmodel import Field, Relationship
from management_server.models.helpers import EmailString
from management_server.models.validators import phone_number_vaidator
from management_server.models.base import BaseModel, BaseUserModel, BaseStaffModel

def generate_staff_id(dept):
    """
    Generate a unique staff ID by combining the department abbreviation and a randomly generated user number.

    Parameters:
        dept (str): The department abbreviation.

    Returns:
        str: The generated staff ID in the format "AFIT{dept}{user_number}".
    """
    user_number = randint(1000, 9999)
    return f"AFIT{dept}{user_number}"

class UserModel(BaseUserModel, table=True):
    """
    User model class
    """

    __tablename__ = "user"

    first_name: str = Field(max_length=20, min_length=3, nullable=False)
    last_name: str = Field(max_length=20, min_length=3, nullable=False)
    email: EmailString = Field(
        unique=True, nullable=False, max_length=255, min_length=15
    )
    phone_number: str = Field(unique=True, nullable=False, min_length=11, max_length=11)
    mobile_network: str = Field(
        nullable=False, min_length=4, max_length=15, default=None
    )
    state: str = Field(default=None, max_length=50, nullable=False)
    lga: str = Field(default=None, max_length=50, nullable=False)
    ward: str = Field(default=None, max_length=50, nullable=False)
    staff: StaffModel = Relationship(
        back_populates="user", sa_relationship_kwargs={"uselist": False}
    )

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
        # self.i
        """
        Validates the user model before saving it to the database.

        This function is a model validator that is called before saving the user model to the database.
        It performs the following checks:
        - Checks if the 'phone_number' field is empty and raises an assertion error if it is.
        - Checks if the 'mobile_network' field is empty and raises an assertion error if it is.
        - Validates the 'phone_number' field using the 'phone_number_vaidator' function and assigns the result to the 'validate' variable.
        - If the 'validate' variable is None, it raises an error (TODO).
        - Updates the 'mobile_network' field in the data dictionary with the value from the 'validate.network' attribute.

        Parameters:
            data (Dict): The data dictionary containing the user model data.

        Returns:
            Dict: The updated data dictionary with the 'mobile_network' field updated.
        """
        user_phone_number = self.get("phone_numeber", None)
        mobile_network = self.get("mobile_network", None)
        assert user_phone_number is None, "Field phone_numeber is empty"

        assert mobile_network is None, "Field mobile_network is empty"

        validate = phone_number_vaidator(phone_number=user_phone_number)
        if validate is None:
            # TODO raise an error here
            pass
        return data.update(("mobile_network", validate.network))


class DepartmentModel(BaseModel, table=True):
    __tablename__ = "department"
    department_id: str = Field(
        default=None, primary_key=True, nullable=False, index=True
    )
    name: str = Field(max_length=20, min_length=3, nullable=False, unique=True)
    short_name: str = Field(max_length=3, min_length=3, nullable=False, unique=True)
    description: str = Field(max_length=250, min_length=10, nullable=True)
    staff_members: StaffModel = Relationship(back_populates="department")
    department_head: AdminModel = Relationship(
        back_populates="admin", sa_relationship_kwargs={"uselist": False}
    )
    department_head_id: str = Field(
        unique=True, nullable=False, foreign_key="admin.staff_id"
    )


class StaffModel(BaseStaffModel, table=True):
    __tablename__ = "staff"
    staff_id: str = Field(default=None, primary_key=True, nullable=False, index=True)
    user_id: str = Field(foreign_key="user.id", nullable=False, unique=True)
    user: UserModel = Relationship(back_populates="staff")
    department_id: str = Field(
        unique=True, nullable=False, foreign_key="department.department_id"
    )
    department: DepartmentModel = Relationship(
        back_populates="staff_members", sa_relationship_kwargs={"uselist": False}
    )
    department_head_id: str = Field(foreign_key="admin.id", unique=True, nullable=True)
    admin: AdminModel = Relationship(back_populates="staff")

    @model_validator(mode="before")
    def vlidate_staff_model(self, data: Dict):
        department_id = data.get("department_id", None)
        department_id = DepartmentModel.objects().get_one_or_none(key="department_id", value=department_id) 

class AdminModel(BaseStaffModel, table=True):
    __tablename__ = "admin"
    id: str = Field(default=None, primary_key=True, nullable=False, index=True)
    staff_id: str = Field(foreign_key="staff.staff_id", nullable=False, unique=True)
    staff: StaffModel = Relationship(
        back_populates="admin",
        sa_relationship_kwargs={"uselist": False},
    )
