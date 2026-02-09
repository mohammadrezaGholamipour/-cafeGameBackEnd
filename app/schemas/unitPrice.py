from pydantic import BaseModel, Field


class UnitPriceCreate(BaseModel):
    price: int = Field(..., gt=0)

class UnitPriceUpdate(BaseModel):
    price: int | None = Field(None, gt=0)

class UnitPriceWithOutOwner(BaseModel):
    id: int
    price: int
    model_config = {
        "from_attributes": True
    }


class UnitPriceWithOwner(BaseModel):
    id: int
    price: int
    owner_id: int
    owner: "UserWithOutDetails"
    model_config = {
        "from_attributes": True
    }


from app.schemas.user import UserWithOutDetails

UserWithOutDetails.model_rebuild()
