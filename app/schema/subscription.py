from app.schema.base import (
    BaseSchema, 
    BaseRecordSchema
)

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
    user_id: int = None

class SubscriptionSchema(BaseRecordSchema):
    user_id: int
    industry: IndustryEnum
    subcategory: SubcategoryEnum
    source: SourceEnum