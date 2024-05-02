from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.backend.session import create_session
from app.const import (
    AUTH_TAGS,
    AUTH_URL,
)
from app.schema.auth import TokenSchema
from app.schema.auth import (
    CreateUserSchema,
    UserSchema
)
from app.services.auth import AuthService


router = APIRouter(prefix="/" + AUTH_URL, tags=AUTH_TAGS)


@router.post("/token", response_model=TokenSchema)
async def authenticate(
    login: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(create_session),
) -> TokenSchema | None:
    """User authentication. Login should be email.

    Raises:
        HTTPException: 401 Unauthorized
        HTTPException: 404 Not Found

    Returns:
        Access token.
    """

    return AuthService(session).authenticate(login)

@router.post("/register", response_model=UserSchema)
async def register(
    new_user: CreateUserSchema,
    session: Session = Depends(create_session)
) -> UserSchema | None:
    f = AuthService(session).create_user(new_user)
    return f