from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from sqlalchemy import Integer, Enum
import enum


from app.models.base import SQLModel

class IndustryEnum(enum.Enum):
    AGRICULTURE = 1
    AEROSPACE = 2
    CHEMICAL_ENGINEERING = 3
    COMPUTERS = 4
    DEFENSE = 5
    INTERNET = 6
    MANUFACTURING = 7
    PETROLEUM = 8
    TELEVISION = 9

class SourceEnum(enum.Enum):
    BLOGS = 1
    EDUCATION = 2
    NEWSPAPERS = 3
    SOCIAL_MEDIA = 4
    TV_NEWS = 5

class SubcategoryEnum(enum.Enum):
    BANKRUPTCY = 1
    CROWDFUNDING = 2
    MERGERS_AND_ACQUISITIONS = 3
    PRODUCT_RELEASES = 4
    STARTUPS = 5


class SubscriptionModel(SQLModel):
    __tablename__ = "subscriptions"
    __table_args__ = {"schema": "myapi"}

    industry: Mapped[IndustryEnum] = mapped_column("industry")
    source: Mapped[SourceEnum] = mapped_column("source")
    subcategory: Mapped[SubcategoryEnum] = mapped_column("subcategory")