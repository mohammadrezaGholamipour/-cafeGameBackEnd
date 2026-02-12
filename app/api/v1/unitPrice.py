from app.schemas.unitPrice import UnitPriceCreate, UnitPriceWithOwner,UnitPriceWithOutOwner
from fastapi import APIRouter, Depends, HTTPException, status,Path
from app.core.security import get_current_user
from app.models.unitPrice import UnitPrice
from sqlalchemy.orm import Session
from typing import List, Annotated
from app.db.session import get_db
from app.models.user import User

router = APIRouter(prefix="/api/v1/unit-price", tags=["UnitPrice"], dependencies=[Depends(get_current_user)])


@router.post("/create", response_model=UnitPriceWithOwner, status_code=status.HTTP_201_CREATED)
def create_unit_price(
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
            status_code=status.HTTP_409_CONFLICT,
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
def list_all_unit_price(db: Session = Depends(get_db)):
    unit_prices = db.query(UnitPrice).all()
    return unit_prices



@router.delete(
    "/{unit_price_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_unit_price(
        unit_price_id: Annotated[int, Path(..., gt=0)],
        current_user: Annotated[User, Depends(get_current_user)],
        db: Session = Depends(get_db),
):
    unit_price = db.query(UnitPrice).filter(UnitPrice.id == unit_price_id).first()

    if not unit_price:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"field":"UnitPrice","message": "قیمت واحد مورد نظر وجود ندارد"}
        )

    if unit_price.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"field":"UnitPrice","message": "این قیمت واحد مطعلق به شما نیست و اجازه حذف آن را ندارید"}
        )

    db.delete(unit_price)
    db.commit()

@router.get("/my-unit-price", response_model=list[UnitPriceWithOutOwner])
def list_my_unit_price(
        current_user: Annotated[User, Depends(get_current_user)],
        db: Session = Depends(get_db),
):
    unit_price = (
        db.query(UnitPrice)
        .filter(UnitPrice.owner_id == current_user.id)
        .all()
    )
    return unit_price