from pydantic import BaseModel


class BuffetCreate(BaseModel):
    name: str
    price: int


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
