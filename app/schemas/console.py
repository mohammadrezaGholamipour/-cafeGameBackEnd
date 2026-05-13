from pydantic import BaseModel
from typing import Optional



class ConsoleWithOutOwner(BaseModel):
    id: int
    name: str
    is_deleted:bool
    # type: Optional[str]
    model_config = {
        "from_attributes": True
    }


class ConsoleWithOwner(BaseModel):
    id: int
    name: str
    owner_id: int
    owner:"UserWithOutDetails"
    is_deleted: bool
    model_config = {
        "from_attributes": True
    }

from app.schemas.user import UserWithOutDetails
UserWithOutDetails.model_rebuild()