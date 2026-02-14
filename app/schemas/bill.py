from pydantic import BaseModel
from datetime import datetime


class BillCreate(BaseModel):
    console_id: int
    unit_price_id: int


class BillUpdate(BaseModel):
    console_id: int | None = None
    unit_price_id: int | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    play_price: int | None = None
    total_price: int | None = None


class BillWithOutDetails(BaseModel):
    id: int
    owner_id: int
    console_id: int
    unit_price_id: int
    start_time: datetime
    end_time: datetime | None
    play_price: int | None
    total_price: int | None

    model_config = {
        "from_attributes": True
    }


class BillWithOwner(BaseModel):
    id: int
    owner_id: int
    console: "ConsoleWithOutOwner"
    unit_price: "UnitPriceWithOutOwner"
    owner: "UserWithOutDetails"
    start_time: datetime
    end_time: datetime | None
    play_price: int | None
    total_price: int | None

    model_config = {
        "from_attributes": True
    }


from app.schemas.unitPrice import UnitPriceWithOutOwner
from app.schemas.console import ConsoleWithOutOwner
from app.schemas.buffet import BuffetWithOutOwner
from app.schemas.user import UserWithOutDetails

UnitPriceWithOutOwner.model_rebuild()
ConsoleWithOutOwner.model_rebuild()
BuffetWithOutOwner.model_rebuild()
UserWithOutDetails.model_rebuild()
