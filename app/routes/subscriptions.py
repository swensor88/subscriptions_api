from typing import List, Optional

from fastapi import (
    APIRouter,
    Depends,
    Response
)
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.models.subscription import SubscriptionModel
from app.schema.auth import UserSchema
from app.schema.subscription import(
    SubscriptionSchema,
    SubscriptionSchema
) 
from app.services.subscriptions import SubscriptionService
from app.services.base import (
    BaseDataManager,
    BaseService,
)

from app.backend.session import create_session
from app.services.auth import (
    get_current_user,
    is_admin_user,
    authorize_update
)
from app.exc import raise_with_log


# from backend.session import create_session
from app.const import (
    SUBSCRIPTION_TAGS,
    SUBSCRIPTION_URL,
    SUBSCRIPTION_URL_NEW,
)

from .base import BaseRouter


router = BaseRouter(prefix="/" + SUBSCRIPTION_URL, tags=SUBSCRIPTION_TAGS)


@router.get("/get", response_model=SubscriptionSchema)
async def get_subscription(
    subscription_id: Optional[int] = None,
    user: UserSchema = Depends(get_current_user),
    session: Session = Depends(create_session),
) -> SubscriptionSchema:
    """Get current user's subscription. For admins, option to search subscription by ID if specified. """

    if(subscription_id != None):
        s = SubscriptionService(session).get_subscription(subscription_id)
    else:
        s = SubscriptionService(session).get_user_subscription(user.id)
    return JSONResponse(s.model_dump())


@router.get("/all", response_model=List[SubscriptionSchema])
async def get_all_subscriptions(
    session: Session = Depends(create_session),
    admin = Depends(is_admin_user)
) -> List[SubscriptionSchema]:
    """Get all subscriptions in the database. Admin priveleges required."""

    s = SubscriptionService(session).get_subscriptions()
    d = dict(map(lambda i: (s[i].id, s[i].model_dump()), range(len(s))))
    # return Response(d, 200, {"content-type": "text/json"})
    return JSONResponse(d, status_code=200)

@router.post("/add", response_model = SubscriptionSchema)
async def add_subscription(
    subscription: SubscriptionSchema,
    user: UserSchema = Depends(get_current_user),
    session: Session = Depends(create_session),
) -> SubscriptionSchema:
    """Add subscription. If an admin user wishes to specify user_id, it will create a subscription for that user. 
    Otherwise it will create subscription for currently logged in user.
    """

    s = SubscriptionService(session).add_subscription(subscription, user)
    return JSONResponse(s.model_dump(), status_code=201 if isinstance(s.id, int) else 204)

@router.put("/update")
async def update_subscription(
    subscription: SubscriptionSchema,
    user: UserSchema = Depends(get_current_user),
    session: Session = Depends(create_session)
):
    """Update a subscription. Must be owner of subscription, or have admin priveleges."""
    await authorize_update(subscription, user)

    s = SubscriptionService(session).update_subscription(subscription, user)
    if(isinstance(s, SubscriptionSchema)):
        return JSONResponse(s.model_dump(), status_code=200)
    else:
        return Response(status_code=400)

