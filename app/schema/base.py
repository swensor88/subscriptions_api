from pydantic import (
    BaseModel,
    ConfigDict
)
from typing import Optional
import json



class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    def encode(self,encoding: str = "utf-8", errors: str = "strict"):
        return self.model_dump().encode(encoding, errors)

    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4)

class BaseRecordSchema(BaseSchema):
    id: Optional[int] = None