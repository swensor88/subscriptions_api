from app.schema.base import BaseSchema

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
    industry: IndustryEnum
    subcategory: SubcategoryEnum
    source: SourceEnum