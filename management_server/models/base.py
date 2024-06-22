from datetime import datetime
import uuid as uuid_pkg

from sqlmodel import SQLModel, Field
from pydantic import ConfigDict


class BaseModel(SQLModel):
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
    model_config = ConfigDict(str_strip_whitespace=True, use_enum_values=True)
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4, primary_key=True
    )
