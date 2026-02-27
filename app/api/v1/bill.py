from app.schemas.bill import BillCreate, BillWithOwner, BillWithOutDetails, BillUpdate
from datetime import datetime, timezone, timedelta
from app.core.security import get_current_user
from app.models.unitPrice import UnitPrice
from fastapi import HTTPException, status
from app.models.billFood import BillFood
# from app.core.dropBox import upload_db
from fastapi import APIRouter, Depends
from app.models.console import Console
from app.models.buffet import Buffet
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.models.bill import Bill
from typing import Annotated
from fastapi import Path
from math import ceil

router = APIRouter(
    prefix="/cafe-game-api/v1/bill",
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
        .filter(
            UnitPrice.price == bill_data.unit_price_amount,
            UnitPrice.owner_id == current_user.id
        )
        .first()
    )

    if not unit_price:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"field": "UnitPrice", "message": "قیمت واحد وارد شده وجود ندارد"}
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
    # upload_db()
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


@router.put(
    "/{bill_id}/close",
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
    # upload_db()
    return


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


@router.put("/update-bill/{bill_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_bill(
        bill_id: Annotated[int, Path(..., gt=0)],
        bill_data: BillUpdate,
        current_user: Annotated[User, Depends(get_current_user)],
        db: Session = Depends(get_db),
):
    bill = db.query(Bill).filter(
        Bill.id == bill_id,
        Bill.owner_id == current_user.id
    ).first()

    if not bill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"field": "Bill", "message": "فاکتور یافت نشد"}
        )

    update_data = bill_data.model_dump(exclude_unset=True)

    # تغییر زمان شروع
    if "start_time_offset_minutes" in update_data:
        if bill.end_time is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"field": "Bill", "message": "فاکتور بسته شده است و امکان تغییر زمان وجود ندارد"}
            )

        offset = update_data.pop("start_time_offset_minutes")
        start_time = bill.start_time

        if start_time.tzinfo is None:
            start_time = start_time.replace(tzinfo=timezone.utc)

        bill.start_time = start_time - timedelta(minutes=offset)

    # اضافه یا جایگزینی خوراکی‌ها
    if "foods" in update_data:
        if bill.end_time is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"field": "Bill", "message": "فاکتور بسته شده است و امکان افزودن خوراکی وجود ندارد"}
            )

        foods = update_data.pop("foods")

        # پاک کردن همه خوراکی‌های قبلی
        db.query(BillFood).filter(BillFood.bill_id == bill.id).delete(synchronize_session=False)

        # افزودن خوراکی‌های جدید (حتی اگر لیست خالی باشد، همه قبلی‌ها پاک می‌شوند)
        for food in foods:
            buffet_food = db.query(Buffet).filter(Buffet.id == food["food_id"]).first()
            if not buffet_food:
                raise HTTPException(
                    status_code=404,
                    detail={"field": "Food", "message": "خوراکی یافت نشد"}
                )

            new_bill_food = BillFood(
                bill_id=bill.id,
                food_id=buffet_food.id,
                count=food["count"],
                price=buffet_food.price,
                name=buffet_food.name
            )
            db.add(new_bill_food)

    for key, value in update_data.items():
        setattr(bill, key, value)

    db.commit()
    db.refresh(bill)
    # upload_db()



@router.delete(
    "/remove-bill/{bill_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_bill(
        bill_id: Annotated[int, Path(..., gt=0)],
        current_user: Annotated[User, Depends(get_current_user)],
        db: Session = Depends(get_db)
):
    bill = db.query(Bill).filter(
        Bill.id == bill_id,
        Bill.owner_id == current_user.id
    ).first()

    if not bill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"field": "Bill", "message": "فاکتور یافت نشد"}
        )

    if bill.end_time is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"field": "Bill", "message": "فاکتور بسته شده و نمی‌توان حذف کرد"}
        )

    db.delete(bill)
    db.commit()
    # upload_db()
