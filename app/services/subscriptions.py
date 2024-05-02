from typing import List

from sqlalchemy import select

from app.models.subscription import SubscriptionModel
from app.schema.subscription import SubscriptionSchema
from app.services.base import (
    BaseDataManager,
    BaseService,
)


class SubscriptionService(BaseService):
    def get_subscription(self, subscription_id: int) -> SubscriptionSchema:
        """Get subscription by ID."""

        return SubscriptionDataManager(self.session).get_subscription(subscription_id)

    def get_subscriptions(self, year: int, rating: float) -> List[SubscriptionSchema]:
        """Select subscriptions with filter by ``year`` and ``rating``."""

        return SubscriptionDataManager(self.session).get_subscriptions(year, rating)
    
    def add_subscription(self, subscription: SubscriptionSchema):
        s = SubscriptionModel(
            industry= subscription.industry,
            subcategory= subscription.subcategory,
            source= subscription.source
        )

        return SubscriptionDataManager(self.session).add_subscription(s)


class SubscriptionDataManager(BaseDataManager):
    def get_subscription(self, subscription_id: int) -> SubscriptionSchema:
        stmt = select(SubscriptionModel).where(SubscriptionModel.subscription_id == subscription_id)
        model = self.get_one(stmt)

        return SubscriptionSchema(**model.to_dict())

    def get_subscriptions(self, year: int, rating: float) -> List[SubscriptionSchema]:
        schemas: List[SubscriptionSchema] = list()

        stmt = select(SubscriptionModel).where(
            SubscriptionModel.released >= year,
            SubscriptionModel.rating >= rating,
        )

        for model in self.get_all(stmt):
            schemas += [SubscriptionSchema(**model.to_dict())]

        return schemas
    
    def add_subscription(self, subscription: SubscriptionModel) -> SubscriptionSchema:
        self.add_one(subscription)
        self.session.commit()
        return SubscriptionSchema(
            id=subscription.id,
            industry=subscription.industry,
            subcategory=subscription.subcategory,
            source=subscription.source
        )