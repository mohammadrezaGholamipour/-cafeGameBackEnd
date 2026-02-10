from app.schemas.buffet import BuffetCreate, BuffetWithOutOwner, BuffetWithOwner, BuffetUpdate
from fastapi import APIRouter, Depends, HTTPException, status, Path
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
            detail={"field":"Buffet","message": "برای شما محصولی با این نام قبلاً ثبت شده"}
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


@router.patch("/update/{buffet_id}", response_model=BuffetWithOutOwner,status_code=status.HTTP_200_OK)
def update_buffet(
        current_user: Annotated[User, Depends(get_current_user)],
        payload: BuffetUpdate,
        buffet_id: int = Path(..., gt=0),
        db: Session = Depends(get_db),
):
    buffet = db.query(Buffet).filter(Buffet.id == buffet_id).first()

    if not buffet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"field":"Buffet","message": "محصول مورد نظر پیدا نشد"}
        )
    if buffet.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"field":"Buffet","message": "این محصول مطعلق به شما نیست و اجازه حذف آن را ندارید"}
        )

    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(buffet, field, value)

    db.commit()
    db.refresh(buffet)
    return buffet


@router.get("/list", response_model=List[BuffetWithOwner])
def list_buffets(db: Session = Depends(get_db)):
    buffets = db.query(Buffet).all()
    return buffets

@router.delete(
    "/{buffet_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_buffet(
        buffet_id: Annotated[int, Path(..., gt=0)],
        current_user: Annotated[User, Depends(get_current_user)],
        db: Session = Depends(get_db),
):
    buffet = db.query(Buffet).filter(Buffet.id == buffet_id).first()

    if not buffet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"field":"Buffet","message": "همچین موردی وجود ندارد"}
        )

    if buffet.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"field":"Buffet","message": "این مورد متعلق به شما نیست و امکان حذف آن برای شما وجود ندارد"}
        )

    db.delete(buffet)
    db.commit()
