from datetime import (
    datetime,
    timedelta,
)
from typing import Callable

from fastapi import (
    Depends,
    status,
)
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)
from jose import (
    jwt,
    JWTError,
)
from passlib.context import CryptContext
from sqlalchemy import select

from app.backend.config import config
from app.const import (
    AUTH_URL,
    AUTH_TOKEN_PATH,
    TOKEN_ALGORITHM,
    TOKEN_EXPIRE_MINUTES,
    TOKEN_TYPE,
)
from app.exc import raise_with_log
from app.models.auth import UserModel
from app.schema.auth import (
    CreateUserSchema,
    TokenSchema,
    UserSchema,
)
from app.services.base import (
    BaseDataManager,
    BaseService,
)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_schema = OAuth2PasswordBearer(tokenUrl=AUTH_URL + "/" + AUTH_TOKEN_PATH, auto_error=False)


async def get_current_user(token: str = Depends(oauth2_schema)) -> UserSchema | None:
    """Decode token to obtain user information.

    Extracts user information from token and verifies expiration time.
    If token is valid then instance of :class:`~app.schemas.auth.UserSchema`
    is returned, otherwise exception is raised.

    Args:
        token:
            The token to verify.

    Returns:
        Decoded user dictionary.
    """

    if token is None:
        raise_with_log(status.HTTP_401_UNAUTHORIZED, "Invalid token")

    try:
        # decode token using secret token key provided by config
        payload = jwt.decode(token, config.token_key, algorithms=[TOKEN_ALGORITHM])

        # extract encoded information
        id: str = payload.get("id")
        email: str = payload.get("email")
        expires_at: str = payload.get("expires_at")

        if id is None:
            raise_with_log(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")

        if is_expired(expires_at):
            raise_with_log(status.HTTP_401_UNAUTHORIZED, "Token expired")

        return UserSchema(id=id, email=email)
    except JWTError:
        raise_with_log(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")

    return None

async def is_admin_user(user: UserSchema = Depends(get_current_user)) -> bool | None:
    """
    Check for admin user. Raises exception with 401 if not admin
    \nReturns: 
    \n-True if admin is logged in
    \n-False is regular user is logged in
    \n-None if not logged in
    """
    if(user == None or user.admin == None or not user.admin):
        raise_with_log(status.HTTP_401_UNAUTHORIZED, "Must be admin user")
    else:
        return True

def is_expired(expires_at: str) -> bool:
    """Return :obj:`True` if token has expired."""

    return datetime.strptime(expires_at, "%Y-%m-%d %H:%M:%S") < datetime.utcnow()


class HashingMixin:
    """Hashing and verifying passwords."""

    @staticmethod
    def bcrypt(password: str) -> str:
        """Generate a bcrypt hashed password."""

        return pwd_context.hash(password)

    @staticmethod
    def verify(hashed_password: str, plain_password: str) -> bool:
        """Verify a password against a hash."""

        return pwd_context.verify(plain_password, hashed_password)


class AuthService(HashingMixin, BaseService):
    """Authentication service."""

    def create_user(self, user: CreateUserSchema) -> UserSchema:
        """Add user with hashed password to database."""

        user_model = UserModel(
            email=user.email,
            admin=user.admin,
            hashed_password=self.bcrypt(user.password),
        )

        return AuthDataManager(self.session).add_user(user_model)

    def authenticate(
        self, login: OAuth2PasswordRequestForm = Depends()
    ) -> TokenSchema | None:
        """Generate token.

        Obtains username and password and verifies password against
        hashed password stored in database. If valid then temporary
        token is generated, otherwise the corresponding exception is raised.
        """

        user = AuthDataManager(self.session).get_user(login.username)

        if user.hashed_password is None:
            raise_with_log(status.HTTP_401_UNAUTHORIZED, "Incorrect password")
        else:
            if not self.verify(user.hashed_password, login.password):
                raise_with_log(status.HTTP_401_UNAUTHORIZED, "Incorrect password")
            else:
                access_token = self._create_access_token(user.id, user.email)
                return TokenSchema(access_token=access_token, token_type=TOKEN_TYPE)
        return None

    def _create_access_token(self, id: int, email: str) -> str:
        """Encode user information and expiration time."""

        payload = {
            "id": id,
            "email": email,
            "expires_at": self._expiration_time(),
        }

        return jwt.encode(payload, config.token_key, algorithm=TOKEN_ALGORITHM)

    @staticmethod
    def _expiration_time() -> str:
        """Get token expiration time."""

        expires_at = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
        return expires_at.strftime("%Y-%m-%d %H:%M:%S")


class AuthDataManager(BaseDataManager):
    def add_user(self, user: UserModel) -> UserSchema:
        """Write user to database."""

        self.add_one(user)
        self.session.commit()
        return UserSchema(
            id=user.id,
            admin=user.admin,
            email=user.email
        )

    def get_user(self, email: str) -> UserSchema:
        """Read user from database."""

        model = self.get_one(select(UserModel).where(UserModel.email == email))

        if not isinstance(model, UserModel):
            raise_with_log(status.HTTP_404_NOT_FOUND, "User not found")

        r = UserSchema(
            id=model.id,
            admin=model.admin,
            email=model.email,
            hashed_password=model.hashed_password,
        )
        return r