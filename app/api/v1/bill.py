from fastapi import APIRouter, Depends, status, HTTPException, Path
from sqlalchemy.orm import Session
from datetime import datetime, UTC
from typing import Annotated

from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.bill import Bill

from app.schemas.bill import BillCreate, BillUpdate, BillWithOutOwner

router = APIRouter(
    prefix="/api/v1/bill",
    tags=["Bill"],
    dependencies=[Depends(get_current_user)]
)


def create_bill(
        bill_data: BillCreate,
        current_user: Annotated[User, Depends(get_current_user)],
        db: Session = Depends(get_db),
):
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
