from typing import List

from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.orm import Session

from app.models.subscription import SubscriptionModel
from app.schema.auth import UserSchema
from app.schema.subscription import(
    SubscriptionSchema,
    CreateSubscriptionSchema
) 
from app.services.subscriptions import SubscriptionService
from app.services.base import (
    BaseDataManager,
    BaseService,
)

from app.backend.session import create_session
from app.services.auth import get_current_user


# from backend.session import create_session
from app.const import (
    SUBSCRIPTION_TAGS,
    SUBSCRIPTION_URL,
    SUBSCRIPTION_URL_NEW,
)

from .base import BaseRouter


router = BaseRouter(prefix="/" + SUBSCRIPTION_URL, tags=SUBSCRIPTION_TAGS)


@router.get("/", response_model=SubscriptionSchema)
async def get_subscription(
    subscription_id: int,
    user: UserSchema = Depends(get_current_user),
    session: Session = Depends(create_session),
) -> SubscriptionSchema:
    """Get subscription by ID."""

    return SubscriptionService(session).get_subscription(subscription_id)

@router.post("/add", response_model = SubscriptionSchema)
async def add_subscription(
    subscription: CreateSubscriptionSchema,
    session: Session = Depends(create_session),
) -> SubscriptionSchema:
    """Get movies by ``year`` and ``rating``."""

    return SubscriptionService(session).add_subscription(subscription)
