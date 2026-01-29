from app.schemas.unitPrice import UnitPriceWithOutUser, UnitPriceCreate, UnitPriceWithUser
from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_user
from app.models.unitPrice import UnitPrice
from sqlalchemy.orm import Session
from typing import List, Annotated
from app.db.session import get_db
from app.models.user import User

router = APIRouter(prefix="/api/v1/unitPrice", tags=["UnitPrice"], dependencies=[Depends(get_current_user)])


@router.post("/create", response_model=UnitPriceWithOutUser, status_code=201)
def create_buffet(
        current_user: Annotated[User, Depends(get_current_user)],
        unitPrice: UnitPriceCreate,
        db: Session = Depends(get_db),
):
    exists = db.query(UnitPrice.id).filter(
        UnitPrice.owner_id == current_user.id,
        UnitPrice.price == UnitPrice.price
    ).first()

    if exists:
        raise HTTPException(
            status_code=409,
            detail={
                "field": "name",
                "message": "برای شما محصولی با این نام قبلاً ثبت شده"
            }

        )
    new_unit_price = UnitPrice(
        name=unitPrice.name,
        price=unitPrice.price,
        owner=current_user
    )
    db.add(new_unit_price)
    db.commit()
    db.refresh(new_unit_price)
    return new_unit_price


@router.get("/list", response_model=List[UnitPriceWithUser])
def list_buffets(db: Session = Depends(get_db)):
    unit_prices = db.query(UnitPrice).all()
    return unit_prices
