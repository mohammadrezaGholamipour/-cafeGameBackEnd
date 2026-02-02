from app.schemas.unitPrice import UnitPriceWithOutOwner, UnitPriceCreate, UnitPriceWithOwner
from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_user
from app.models.unitPrice import UnitPrice
from sqlalchemy.orm import Session
from typing import List, Annotated
from app.db.session import get_db
from app.models.user import User

router = APIRouter(prefix="/api/v1/unitPrice", tags=["UnitPrice"], dependencies=[Depends(get_current_user)])


@router.post("/create", response_model=UnitPriceWithOwner, status_code=201)
def create_buffet(
        current_user: Annotated[User, Depends(get_current_user)],
        unit_price: UnitPriceCreate,
        db: Session = Depends(get_db),
):
    exists = db.query(UnitPrice.id).filter(
        UnitPrice.owner_id == current_user.id,
        UnitPrice.price == unit_price.price
    ).first()

    if exists:
        raise HTTPException(
            status_code=409,
            detail={
                "field": "price",
                "message": "قبلا قیمت واحد با این مقدار ایجاد شده است"
            }

        )
    new_unit_price = UnitPrice(
        price=unit_price.price,
        owner=current_user
    )
    db.add(new_unit_price)
    db.commit()
    db.refresh(new_unit_price)
    return new_unit_price


@router.get("/list", response_model=List[UnitPriceWithOwner])
def list_buffets(db: Session = Depends(get_db)):
    unit_prices = db.query(UnitPrice).all()
    return unit_prices
