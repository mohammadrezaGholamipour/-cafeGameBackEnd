from pydantic import BaseModel


class ConsoleCreate(BaseModel):
    name: str


class ConsoleWithOutUser(BaseModel):
    id: int
    name: str
    model_config = {
        "from_attributes": True
    }


class ConsoleWithUser(BaseModel):
    id: int
    name: str
    owner:"UserWithOutDetails"
    model_config = {
        "from_attributes": True
    }

from app.schemas.user import UserWithOutDetails
UserWithOutDetails.model_rebuild()