from pydantic import BaseModel

class BillFoodItem(BaseModel):
    food_id: int
    count: int


class BillFoodWithOutDetails(BaseModel):
    id: int
    food_id: int
    bill_id: int
    count: int
    price: int
    name: str

    model_config = {
        "from_attributes": True
    }
