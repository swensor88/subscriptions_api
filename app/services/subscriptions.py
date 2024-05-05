from typing import List
from fastapi import (
    Depends,
    status,
)
from sqlalchemy import(
    select, 
    update
)

from app.models.subscription import SubscriptionModel
from app.schema.subscription import SubscriptionSchema, UserSchema
from app.services.base import (
    BaseDataManager,
    BaseService,
)

from app.exc import raise_with_log

class SubscriptionService(BaseService):
    def get_subscription(self, subscription_id: int) -> SubscriptionSchema:
        """Get subscription by ID."""

        return SubscriptionDataManager(self.session).get_subscription(subscription_id)
    
    def get_user_subscription(self, user_id: int) -> SubscriptionSchema:
        return SubscriptionDataManager(self.session).get_subscription_by_user_id(user_id)

    def get_subscriptions(self) -> List[SubscriptionSchema]:
        """Select all subscriptions. Admin only."""

        return SubscriptionDataManager(self.session).get_subscriptions()
    
    def add_subscription(self, subscription: SubscriptionSchema, user: UserSchema):

        if(self.user_has_subscription(user.id) or self.user_has_subscription(subscription.user_id)):
            raise raise_with_log(status.HTTP_400_BAD_REQUEST, "Subscription already exists for user. Update existing subscription")

        s = SubscriptionModel(
            industry=subscription.industry,
            subcategory=subscription.subcategory,
            source=subscription.source,
            user_id=subscription.user_id if isinstance(subscription.user_id, int) and user.admin else user.id 
        )

        return SubscriptionDataManager(self.session).add_subscription(s)
    
    def user_has_subscription(self, user_id: int) -> bool:
        s = SubscriptionDataManager(self.session).get_subscription_by_user_id(user_id)
        if(isinstance(s, SubscriptionSchema)):
            return True
        else:
            return False
        
    def update_subscription(self, subscription: SubscriptionSchema, user: UserSchema) -> SubscriptionSchema:
        return SubscriptionDataManager(self.session).update_subscription(
            SubscriptionModel(
                id=subscription.id,
                industry=subscription.industry,
                subcategory=subscription.subcategory,
                source=subscription.source,
                user_id=subscription.user_id
            )
        )


class SubscriptionDataManager(BaseDataManager):
    def get_subscription(self, subscription_id: int) -> SubscriptionSchema:
        stmt = select(SubscriptionModel).where(SubscriptionModel.id == subscription_id)
        model = self.get_one(stmt)

        if not isinstance(model, SubscriptionModel):
            raise_with_log(status.HTTP_404_NOT_FOUND, "Subscription not found")

        return SubscriptionSchema(**model.to_dict())
    
    def get_subscription_by_user_id(self, user_id: int) -> SubscriptionSchema | None:
        stmt = select(SubscriptionModel).where(SubscriptionModel.user_id == user_id)
        model = self.get_one(stmt)

        if not isinstance(model, SubscriptionModel):
            return None

        return SubscriptionSchema(**model.to_dict())

    def get_subscriptions(self) -> List[SubscriptionSchema]:
        schemas: List[SubscriptionSchema] = list()

        stmt = select(SubscriptionModel)

        for model in self.get_all(stmt):
            schemas+= [SubscriptionSchema(**model.to_dict())]

        return schemas
    
    def add_subscription(self, subscription: SubscriptionModel) -> SubscriptionSchema:
        self.add_one(subscription)
        self.session.commit()
        return SubscriptionSchema(
            id=subscription.id,
            industry=subscription.industry,
            subcategory=subscription.subcategory,
            source=subscription.source,
            user_id=subscription.user_id
        )
    
    def update_subscription(self, subscription: SubscriptionModel) -> SubscriptionSchema | None:
        if(subscription.id == None):
            raise_with_log(status.HTTP_400_BAD_REQUEST, "Missing 'id' field from Subscription entity in payload.")

        stmt = select(SubscriptionModel).where(SubscriptionModel.id == subscription.id)
        model = self.get_one(stmt)

        if subscription.source != None:
            model.source = subscription.source 
        if subscription.subcategory != None:
            model.subcategory = subscription.subcategory 
        if subscription.industry != None:
            model.industry = subscription.industry 
        if subscription.user_id != None:
            model.user_id = subscription.user_id  

        self.add_one(model)
        self.session.commit()

        return SubscriptionSchema(
            id=subscription.id,
            industry=subscription.industry,
            subcategory=subscription.subcategory,
            source=subscription.source,
            user_id=subscription.user_id
        )