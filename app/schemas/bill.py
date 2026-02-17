from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class BillCreate(BaseModel):
    console_id: int
    unit_price_amount: int


class BillUpdate(BaseModel):
    console_id: int | None = None
    unit_price_amount: int | None = None
    start_time: datetime | None = None

class BillWithOutDetails(BaseModel):
    id: int
    owner_id: int
    console_id: int
    unit_price_amount: int
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
    unit_price_amount: "UnitPriceWithOutOwner"
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
