from pydantic import (
    BaseModel,
    ConfigDict
)
from typing import Optional



class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class BaseRecordSchema(BaseSchema):
    id: Optional[int] = None