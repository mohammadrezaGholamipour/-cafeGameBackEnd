from app.models.console import Console
from app.models.unitPrice import UnitPrice
from app.schemas.bill import BillCreate, BillWithOwner, BillWithOutDetails
from app.core.security import get_current_user
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, UTC
from app.db.session import get_db
from app.models.user import User
from app.models.bill import Bill
from typing import Annotated

router = APIRouter(
    prefix="/api/v1/bill",
    tags=["Bill"],
    dependencies=[Depends(get_current_user)]
)

from fastapi import HTTPException, status


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
    # 1️⃣ چک کن کنسول وجود داشته باشد
    console = (
        db.query(Console)
        .filter(Console.id == bill_data.console_id)
        .first()
    )

    if not console:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"field": "Console", "message": "دستگاه یافت نشد"}
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
        .filter(UnitPrice.id == bill_data.unit_price_id)
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
        console_id=bill_data.console_id,
        unit_price_id=bill_data.unit_price_id,
        start_time=datetime.now(UTC)
    )

    db.add(new_bill)
    db.commit()
    db.refresh(new_bill)

    return new_bill


@router.get(
    "/list",
    response_model=list[BillWithOwner]
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

# @router.get(
#     "/my-bills",
#     response_model=list[BillOut]
# )
# def list_my_bills(
#         current_user: Annotated[User, Depends(get_current_user)],
#         db: Session = Depends(get_db),
# ):
#     bills = (
#         db.query(Bill)
#         .filter(Bill.owner_id == current_user.id)
#         .all()
#     )
#     return bills
#
#
# @router.patch(
#     "/{bill_id}",
#     response_model=BillOut
# )
# def update_bill(
#         bill_id: Annotated[int, Path(..., gt=0)],
#         bill_data: BillUpdate,
#         current_user: Annotated[User, Depends(get_current_user)],
#         db: Session = Depends(get_db),
# ):
#     bill = db.query(Bill).filter(Bill.id == bill_id).first()
#
#     if not bill:
#         raise HTTPException(status_code=404, detail="فاکتور یافت نشد")
#
#     if bill.owner_id != current_user.id:
#         raise HTTPException(status_code=403, detail="اجازه دسترسی ندارید")
#
#     for key, value in bill_data.dict(exclude_unset=True).items():
#         setattr(bill, key, value)
#
#     db.commit()
#     db.refresh(bill)
#
#     return bill
#
#
# @router.delete(
#     "/{bill_id}",
#     status_code=status.HTTP_204_NO_CONTENT
# )
# def delete_bill(
#         bill_id: Annotated[int, Path(..., gt=0)],
#         current_user: Annotated[User, Depends(get_current_user)],
#         db: Session = Depends(get_db),
# ):
#     bill = db.query(Bill).filter(Bill.id == bill_id).first()
#
#     if not bill:
#         raise HTTPException(status_code=404, detail="فاکتور یافت نشد")
#
#     if bill.owner_id != current_user.id:
#         raise HTTPException(status_code=403, detail="اجازه دسترسی ندارید")
#
#     db.delete(bill)
#     db.commit()
#
#
# @router.get(
#     "/list",
#     response_model=list[BillOut]
# )
# def list_all_bills(
#         db: Session = Depends(get_db),
# ):
#     bills = (
#         db.query(Bill)
#         .order_by(Bill.id.desc())
#         .all()
#     )
#     return bills
