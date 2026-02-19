from app.schemas.bill import BillCreate, BillWithOwner, BillWithOutDetails
from app.core.security import get_current_user
from app.models.unitPrice import UnitPrice
from fastapi import HTTPException, status
from fastapi import APIRouter, Depends
from app.models.console import Console
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.db.session import get_db
from app.models.user import User
from app.models.bill import Bill
from typing import Annotated
from fastapi import Path
from math import ceil

router = APIRouter(
    prefix="/api/v1/bill",
    tags=["Bill"],
    dependencies=[Depends(get_current_user)]
)


@router.post(
    "/create",
    response_model=BillWithOutDetails,
    status_code=status.HTTP_201_CREATED
)
def create_bill(
        bill_data: BillCreate,
        current_user: Annotated[User, Depends(get_current_user)],
        db: Session = Depends(get_db),
):
    console = (
        db.query(Console)
        .filter(
            Console.id == bill_data.console_id,
            Console.is_deleted == False
        )
        .first()
    )

    if not console:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"field": "Console", "message": "دستگاه یافت نشد یا حذف شده است"}
        )

    if console.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"field": "Console", "message": "این دستگاه متعلق به شما نیست"}
        )

    active_bill = (
        db.query(Bill)
        .filter(
            Bill.console_id == console.id,
            Bill.end_time.is_(None)
        )
        .first()
    )

    if active_bill:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"field": "Bill", "message": "برای این دستگاه یک فاکتور باز وجود دارد"}
        )

    unit_price = (
        db.query(UnitPrice)
        .filter(UnitPrice.price == bill_data.unit_price_amount)
        .first()
    )

    if not unit_price:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"field": "UnitPrice", "message": "قیمت واحد یافت نشد"}
        )

    if unit_price.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"field": "UnitPrice", "message": "این قیمت واحد متعلق به شما نیست"}
        )

    new_bill = Bill(
        owner_id=current_user.id,
        console_id=console.id,
        unit_price_amount=unit_price.price,
        start_time=datetime.now(timezone.utc)
    )

    db.add(new_bill)
    db.commit()
    db.refresh(new_bill)

    return new_bill


@router.get(
    "/list",
    response_model=list[BillWithOwner],
    status_code=status.HTTP_200_OK
)
def list_all_bills(
        db: Session = Depends(get_db),
):
    bills = (
        db.query(Bill)
        .order_by(Bill.id.desc())
        .all()
    )
    return bills


@router.get(
    "/my-bills",
    response_model=list[BillWithOutDetails],
    status_code=status.HTTP_200_OK

)
def list_my_bills(
        current_user: Annotated[User, Depends(get_current_user)],
        db: Session = Depends(get_db),
):
    bills = (
        db.query(Bill)
        .filter(Bill.owner_id == current_user.id)
        .all()
    )
    return bills


@router.patch(
    "/{bill_id}/close",
    response_model=BillWithOutDetails,
    status_code=status.HTTP_204_NO_CONTENT
)
def close_bill(
        bill_id: Annotated[int, Path(..., gt=0)],
        current_user: Annotated[User, Depends(get_current_user)],
        db: Session = Depends(get_db),
):
    bill = (
        db.query(Bill)
        .filter(
            Bill.id == bill_id,
            Bill.owner_id == current_user.id
        )
        .first()
    )

    if not bill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"field": "Bill", "message": "فاکتور یافت نشد"}
        )

    if bill.end_time is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"field": "Bill", "message": "این فاکتور قبلا بسته شده است"}
        )

    now = datetime.now(timezone.utc)

    start_time = bill.start_time
    if start_time.tzinfo is None:
        start_time = start_time.replace(tzinfo=timezone.utc)

    duration_seconds = (now - start_time).total_seconds()
    duration_hours = duration_seconds / 3600

    if duration_hours <= 1:
        raw_price = bill.unit_price_amount
    else:
        raw_price = duration_hours * bill.unit_price_amount

    rounded_price = ceil(raw_price / 1000) * 1000

    bill.end_time = now
    bill.play_price = int(rounded_price)
    bill.total_price = int(rounded_price)

    db.commit()
    db.refresh(bill)


@router.get(
    "/my-open-bills",
    response_model=list[BillWithOutDetails],
    status_code=status.HTTP_200_OK
)
def list_my_open_bills(
        current_user: Annotated[User, Depends(get_current_user)],
        db: Session = Depends(get_db),
):
    open_bills = (
        db.query(Bill)
        .filter(
            Bill.owner_id == current_user.id,
            Bill.end_time.is_(None)
        )
        .order_by(Bill.id.desc())
        .all()
    )

    return open_bills
