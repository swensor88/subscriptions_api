from app.schema.base import BaseSchema


class CreateUserSchema(BaseSchema):
    email: str
    password: str
    admin: bool = False


class UserSchema(BaseSchema):
    email: str
    admin: bool
    hashed_password: str | None = None


class TokenSchema(BaseSchema):
    access_token: str
    token_type: str