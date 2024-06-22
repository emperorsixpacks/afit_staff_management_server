from email_validator import validate_email

from pydantic import EmailStr


class EmailString(EmailStr):

    @classmethod
    def _validate(cls, input_value: str, /) -> str:
        return validate_email(input_value, check_deliverability=True)[1]
