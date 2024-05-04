from typing import (
    Any,
    Dict,
    List,
)

import datetime

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column
)
from sqlalchemy.sql import func
from sqlalchemy import (
    Integer, 
    String, 
    DateTime
)


class SQLModel(DeclarativeBase):
    """Base class used for model definitions.

    Provides convenience methods that can be used to convert model
    to the corresponding schema.
    """
    id: Mapped[int] = mapped_column("id", primary_key = True)
    # created_at: Mapped[datetime.datetime] = mapped_column("created_at", DateTime(timezone=True), server_default=func.now())
    # updated_at: Mapped[datetime.datetime] = mapped_column("created_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.current_timestamp())

    @classmethod
    def schema(cls) -> str:
        """Return name of database schema the model refers to."""

        _schema = cls.__mapper__.selectable.schema
        if _schema is None:
            raise ValueError("Cannot identify model schema")
        return _schema

    @classmethod
    def table_name(cls) -> str:
        """Return name of the table the model refers to."""

        return cls.__tablename__

    @classmethod
    def fields(cls) -> List[str]:
        """Return list of model field names."""

        return cls.__mapper__.selectable.c.keys()

    def to_dict(self) -> Dict[str, Any]:
        """Convert model instance to a dictionary."""

        _dict: Dict[str, Any] = dict()
        for key in self.__mapper__.c.keys():
            _dict[key] = getattr(self, key)
        return _dict