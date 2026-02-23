from fastapi import APIRouter, Depends, status, HTTPException, Path

from app.core.dropBox import upload_db
from app.schemas.console import ConsoleWithOwner,ConsoleWithOutOwner
from app.core.security import get_current_user
from app.models.console import Console
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from typing import Annotated

router = APIRouter(prefix="/api/v1/console", tags=["Console"], dependencies=[Depends(get_current_user)])


@router.post(
    "/create",
    response_model=ConsoleWithOwner,
    status_code=status.HTTP_201_CREATED,
)
def create_console(
        current_user: Annotated[User, Depends(get_current_user)],
        db: Session = Depends(get_db),
):
    active_numbers = (
        db.query(Console.name)
        .filter(
            Console.owner_id == current_user.id,
            Console.is_deleted == False
        )
        .all()
    )

    used_numbers = {int(row[0]) for row in active_numbers}

    next_number = 1
    while next_number in used_numbers:
        next_number += 1

    new_console = Console(
        name=str(next_number),
        owner=current_user
    )

    db.add(new_console)
    db.commit()
    db.refresh(new_console)
    upload_db()
    return new_console



@router.get("/list", response_model=list[ConsoleWithOwner])
def list_all_consoles(db: Session = Depends(get_db)):
    consoles = db.query(Console).all()
    return consoles


@router.delete(
    "/{console_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_console(
        console_id: Annotated[int, Path(..., gt=0)],
        current_user: Annotated[User, Depends(get_current_user)],
        db: Session = Depends(get_db),
):
    console = (
        db.query(Console)
        .filter(Console.id == console_id)
        .first()
    )

    if not console:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"field": "Console", "message": "دستگاه مورد نظر وجود ندارد"}
        )

    if console.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"field": "Console", "message": "این دستگاه متعلق به شما نیست"}
        )

    if console.is_deleted:
        return

    console.is_deleted = True
    db.commit()
    upload_db()


@router.get("/my-console", response_model=list[ConsoleWithOutOwner])
def list_my_consoles(
        current_user: Annotated[User, Depends(get_current_user)],
        db: Session = Depends(get_db),
):
    consoles = (
        db.query(Console)
        .filter(Console.owner_id == current_user.id)
        .all()
    )
    return consoles
