from pydantic import BaseModel


class ConsoleWithOutUser(BaseModel):
    id: int
    name: str
    model_config = {
        "from_attributes": True
    }


class ConsoleWithUser(BaseModel):
    id: int
    name: str
    owner_id: int
    owner:"UserWithOutDetails"
    model_config = {
        "from_attributes": True
    }

from app.schemas.user import UserWithOutDetails
UserWithOutDetails.model_rebuild()