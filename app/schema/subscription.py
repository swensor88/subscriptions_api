from app.schema.base import BaseSchema
from app.schema.auth import UserSchema

from app.models.subscription import(
    IndustryEnum,
    SubcategoryEnum,
    SourceEnum
)

import enum

class CreateSubscriptionSchema(BaseSchema):
    industry: IndustryEnum
    subcategory: SubcategoryEnum
    source: SourceEnum

class SubscriptionSchema(BaseSchema):
    id: int
    user: UserSchema
    industry: IndustryEnum
    subcategory: SubcategoryEnum
    source: SourceEnum