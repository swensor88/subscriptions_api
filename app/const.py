from enum import Enum
from typing import (
    Final,
    List,
)


# Open API parameters
OPEN_API_TITLE: Final = "Subscriptions API"
OPEN_API_DESCRIPTION: Final = "Demo Subscriptions API for NWO.ai built with FastAPI."

# Authentication service constants
AUTH_TAGS: Final[List[str | Enum] | None] = ["Authentication"]
AUTH_URL: Final = "auth"
AUTH_TOKEN_PATH: Final = "token"

TOKEN_TYPE: Final = "bearer"
TOKEN_EXPIRE_MINUTES: Final = 60

# Algorithm used to sign the JWT tokens
TOKEN_ALGORITHM: Final = "HS512"

# Subscription service constants
SUBSCRIPTION_TAGS: Final[List[str | Enum] | None] = ["Subscriptions"]
SUBSCRIPTION_URL: Final = "subscriptions"
SUBSCRIPTION_URL_NEW: Final = "new"