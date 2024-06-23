from __future__ import annotations
from datetime import datetime
from typing import TypeVar, Generic
import uuid as uuid_pkg
from dataclasses import dataclass

from sqlmodel import SQLModel, Field, select
from sqlmodel.orm.session import Session
from pydantic import ConfigDict

from management_server.server.db import get_session

T = TypeVar("T")

@dataclass
class BaseManager(Generic[T]):
    model: T
    session: Session = Field(default_factory=get_session)
    def get_one_or_none(self, default=None, **kwargs) -> T | None:
        """
        Retrieves a single record from the database based on the given key-value pair.

        Parameters:
            key (Any): The key to search for in the database.
            value (Any): The value to search for in the database.
            default (Any, optional): The default value to return if no record is found. Defaults to None.

        Returns:
            T | None: The record found in the database, or the default value if no record is found.
        """
        key = kwargs.items()[0][0]
        value = kwargs.get(key, None)
        statement = select(self.model).where(key == value)
        result = self._run(statement).one_or_none()
        return result

    def _run(self, *args, **kwargs):
        try:
            with self.session.begin():
                return self.session.exec(*args, **kwargs)
        except Exception as e:
            self.session.rollback()
            raise e
        

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
    
    @classmethod
    def objects(cls) -> BaseManager:
        return BaseManager(model=cls)

class BaseUserModel(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, use_enum_values=True, arbitrary_types_allowed=True)
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4, primary_key=True
    )


class BaseStaffModel(BaseModel):
    pass



# TODO ValueError: <class 'management_server.models.models.DepartmentModel'> has no matching SQLAlchemy type
