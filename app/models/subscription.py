from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from sqlalchemy import Integer, Enum
import enum

from app.models.base import SQLModel

class SubscriptionModel(SQLModel):
    __tablename__ = "subscriptions"
    __table_args__ = {"schema": "public"}

    industry: Mapped[str] = mapped_column("industry")
    source: Mapped[str] = mapped_column("source")
    subcategory: Mapped[str] = mapped_column("subcategory")
    user_id: Mapped[int] = mapped_column("user_id")