from __future__ import annotations
from pydantic import Field, ConfigDict

from management_server.models.helpers import EmailString

from management_server.models import BaseModel

class UserModel(BaseModel, table=True):
    """
    User model class
    """

    model_config = ConfigDict(
        extra="forbid", str_strip_whitespace=True, use_enum_values=True
    )
    first_name: str = Field(max_length=20, min_length=3, nullable=False)
    last_name: str = Field(max_length=20, min_length=3, nullable=False)
    email: EmailString = Field(unique=True, nullable=False, max_length=255, min_length=15)
    phone_number: str = Field(unique=True, nullable=False, min_length=11, max_length=11)
    state: str = Field(default=None, max_length=50, nullable=False)
    lga: str = Field(default=None, max_length=50, nullable=False)
    ward: str = Field(default=None, max_length=50, nullable=False)

     @property
    def full_name(self):
        """
        Returns the full name of the object.

        Returns:
            str: The full name of the object.
        """
        return f"{self.first_name} {self.last_name}"


    @field_validator("identification_type")
    @classmethod
    def check_identification_type(cls, value: str):
        """
        Validates the identification type.

        Args:
            cls (Any): The class object.
            value (str): The value to be validated.

        Raises:
            InvalidRequestError: If the value is not a valid identification type.

        Returns:
            str: The validated identification type.
        """
        identification_types = [i.name for i in IdentificationType]
        if value not in identification_types:
            raise InvalidRequestError(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=f"identification type should be {', '.join(identification_types)}",
            )
        return value

    @field_validator("identification_number", mode="before")
    @classmethod
    def check_valid_identification_number(cls, value: str):
        """
        Check if the given identification number is valid.

        This function takes in a string value representing an identification number and checks if it is a valid integer. If the value is not a valid integer, an InvalidRequestError is raised with the appropriate status code and detail message. Otherwise, the value is converted to a string and returned.

        Parameters:
        - value (str): The identification number to be checked.

        Returns:
        - str: The identification number as a string if it is valid.

        Raises:
        - InvalidRequestError: If the identification number is not a valid integer.
        """
        try:
            int(value)
        except ValueError as e:
            raise InvalidRequestError(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Invalid Identification Number",
            ) from e
        return str(value)

    @field_validator("role")
    @classmethod
    def check_valid_user_role(cls, value: str):
        """
        Validates a user role.

        Args:
            value (str): The user role to be validated.

        Raises:
            InvalidRequestError: If the user role is not valid.

        Returns:
            str: The validated user role.
        """
        roles = [i.name for i in Role]
        if value not in roles:
            raise InvalidRequestError(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=f"role type should be {', '.join(roles)}",
            )
        return value

    @field_validator("email")
    @classmethod
    def check_email(cls, value: str):
        """
        Validates an email address.

        Parameters:
            value (str): The email address to be validated.

        Returns:
            str: The validated email address.

        Raises:
            InvalidRequestError: If the email address is invalid.

        Example:
            check_email("test@example.com")
        """
        try:
            # raise an http error here
            return validate_email(value, check_deliverability=True).email
        except (EmailNotValidError, EmailUndeliverableError, EmailSyntaxError) as e:
            raise InvalidRequestError(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid Email"
            ) from e

    @field_validator("phone_number")
    @classmethod
    def check_phone_number(cls, value):
        """
        Check if the given phone number is valid.

        Parameters:
            value (str): The phone number to be checked.

        Returns:
            str: The input phone number if it is valid.

        Raises:
            InvalidRequestError: If the phone number is invalid.

        Note:
            This function validates the phone number by checking if its first four or five digits match any of the mobile prefixes in the system. If the phone number is not valid, an InvalidRequestError with status code 406 (Not Acceptable) and detail message "Invalid Phone Number" is raised.
        """
        first_four_digites = value[:4]
        first_five_digits = value[:5]
        prefixes = [
            prefix
            for prefixes in get_mobile_prefixes().mobile_prefixes
            for prefix in prefixes.prefixes
        ]
        if not (first_four_digites in prefixes or first_five_digits in prefixes):
            raise InvalidRequestError(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Invalid Phone Number",
            )
        return value

class StaffModel(BaseModel, table=True):
    pass

class AdminModel(BaseModel, table=True):
    pass