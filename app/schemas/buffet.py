from pydantic import BaseModel, Field


class BuffetCreate(BaseModel):
    name: str = Field(..., min_length=1)
    price: int = Field(..., gt=0)


class BuffetUpdate(BaseModel):
    name: str | None = Field(None, min_length=1)
    price: int | None = Field(None, gt=0)


class BuffetWithOutOwner(BaseModel):
    id: int
    name: str
    price: int
    model_config = {
        "from_attributes": True
    }


class BuffetWithOwner(BaseModel):
    id: int
    name: str
    price: int
    owner_id: int
    owner: "UserWithOutDetails"
    model_config = {
        "from_attributes": True
    }


from app.schemas.user import UserWithOutDetails

UserWithOutDetails.model_rebuild()
