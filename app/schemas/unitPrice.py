from pydantic import BaseModel


class UnitPriceCreate(BaseModel):
    price: int


class UnitPriceWithOutUser(BaseModel):
    id: int
    price: int
    model_config = {
        "from_attributes": True
    }


class UnitPriceWithUser(BaseModel):
    id: int
    price: int
    owner_id: int
    owner: "UserWithOutDetails"
    model_config = {
        "from_attributes": True
    }


from app.schemas.user import UserWithOutDetails

UserWithOutDetails.model_rebuild()
