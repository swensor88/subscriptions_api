from app.schema.base import (
    BaseSchema, 
    BaseRecordSchema
)
from typing import Optional


class CreateUserSchema(BaseSchema):
    email: str
    password: str
    admin: bool = False


class UserSchema(BaseRecordSchema):
    email: str
    admin: bool | None = None
    hashed_password: Optional[str] | None = None


class TokenSchema(BaseSchema):
    access_token: str
    token_type: str