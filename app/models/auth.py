from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.models.base import SQLModel


class UserModel(SQLModel):
    __tablename__ = "users"
    __table_args__ = {"schema": "public"}

    email: Mapped[str] = mapped_column("email")
    admin: Mapped[bool] = mapped_column("admin")
    hashed_password: Mapped[str] = mapped_column("hashed_password")