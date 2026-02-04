from fastapi import APIRouter, Depends, status, HTTPException, Path
from app.core.security import get_current_user
from app.schemas.user import UserOut, UserUpdatePatch
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from typing import Annotated

router = APIRouter(prefix="/api/v1/user", tags=["User"], dependencies=[Depends(get_current_user)])


@router.get("/list", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.patch("/update", response_model=UserOut)
def update_user(
    payload: UserUpdatePatch,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "کاربر مورد نظر پیدا نشد"}
        )

    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_user(user_id: Annotated[int, Path(..., gt=0)], db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "کاربر مورد نظر پیدا نشد"}
        )

    db.delete(user)
    db.commit()

    return None
