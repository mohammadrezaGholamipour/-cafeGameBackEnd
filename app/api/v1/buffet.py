from app.schemas.buffet import BuffetCreate, BuffetWithOutOwner, BuffetWithOwner
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.security import get_current_user
from app.models.buffet import Buffet
from sqlalchemy.orm import Session
from typing import List, Annotated
from app.db.session import get_db
from app.models.user import User

router = APIRouter(prefix="/api/v1/buffet", tags=["Buffet"], dependencies=[Depends(get_current_user)])


@router.post("/create", response_model=BuffetWithOutOwner, status_code=status.HTTP_201_CREATED)
def create_buffet(
        current_user: Annotated[User, Depends(get_current_user)],
        buffet: BuffetCreate,
        db: Session = Depends(get_db),
):
    exists = db.query(Buffet.id).filter(
        Buffet.owner_id == current_user.id,
        Buffet.name == buffet.name
    ).first()

    if exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "field": "name",
                "message": "برای شما محصولی با این نام قبلاً ثبت شده"
            }

        )
    new_buffet = Buffet(
        name=buffet.name,
        price=buffet.price,
        owner=current_user
    )
    db.add(new_buffet)
    db.commit()
    db.refresh(new_buffet)
    return new_buffet


@router.get("/list", response_model=List[BuffetWithOwner])
def list_buffets(db: Session = Depends(get_db)):
    buffets = db.query(Buffet).all()
    return buffets
