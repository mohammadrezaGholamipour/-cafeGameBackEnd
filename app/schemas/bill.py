from pydantic import BaseModel, field_serializer
from zoneinfo import ZoneInfo
from datetime import datetime

TEHRAN_TZ = ZoneInfo("Asia/Tehran")


class BillCreate(BaseModel):
    console_id: int
    unit_price_amount: int


class BillUpdate(BaseModel):
    unit_price_amount: int | None = None
    start_time_offset_minutes: int | None = None
    payment_method: int | None = None
    foods: list["BillFoodItem"] | None = None


class BillWithOutDetails(BaseModel):
    id: int
    owner_id: int
    console_id: int
    console: "ConsoleWithOutOwner"
    unit_price_amount: int
    start_time: datetime
    end_time: datetime | None
    play_price: int | None
    total_price: int | None
    payment_method: int | None = None
    bill_foods: list["BillFoodWithOutDetails"] = []
    model_config = {
        "from_attributes": True
    }

    @field_serializer("start_time", "end_time")
    def convert_to_tehran(self, value: datetime | None):
        if value is None:
            return None
        return value.astimezone(TEHRAN_TZ).isoformat()


class BillWithOwner(BaseModel):
    id: int
    owner_id: int
    console: "ConsoleWithOutOwner"
    owner: "UserWithOutDetails"
    unit_price_amount: int
    start_time: datetime
    end_time: datetime | None
    play_price: int | None
    total_price: int | None
    payment_method: int | None = None
    bill_foods: list["BillFoodWithOutDetails"] = []
    model_config = {
        "from_attributes": True
    }

    @field_serializer("start_time", "end_time")
    def convert_to_tehran(self, value: datetime | None):
        if value is None:
            return None
        return value.astimezone(TEHRAN_TZ).isoformat()


from app.schemas.billFood import BillFoodWithOutDetails, BillFoodItem
from app.schemas.unitPrice import UnitPriceWithOutOwner
from app.schemas.console import ConsoleWithOutOwner
from app.schemas.buffet import BuffetWithOutOwner
from app.schemas.user import UserWithOutDetails

BillFoodWithOutDetails.model_rebuild()
UnitPriceWithOutOwner.model_rebuild()
ConsoleWithOutOwner.model_rebuild()
BuffetWithOutOwner.model_rebuild()
UserWithOutDetails.model_rebuild()
BillFoodItem.model_rebuild()
