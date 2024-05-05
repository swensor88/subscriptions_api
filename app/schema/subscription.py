from app.schema.base import (
    BaseSchema, 
    BaseRecordSchema
)

from typing import Literal

from app.schema.auth import UserSchema

class SubscriptionSchema(BaseRecordSchema):
    industry: Literal['Agriculture', 'Banking', 'Construction', 'Entertainment', 'Healthcare', 'Hospitality', 'Internet Services', 'Mining', 'Sports', 'Tech']
    subcategory: Literal['Application', 'Mergers and Acquisitions', 'New Products', 'Startups', 'Training']
    source: Literal['Academia', 'Blogs', 'Documentaries', 'Print Media', 'Social Media', 'TV']
    user_id: int = None
