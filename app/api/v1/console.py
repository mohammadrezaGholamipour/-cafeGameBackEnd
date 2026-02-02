from app.schemas.console import ConsoleWithOwner
from app.core.security import get_current_user
from fastapi import APIRouter, Depends
from app.models.console import Console
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from typing import Annotated

router = APIRouter(prefix="/api/v1/console", tags=["Console"], dependencies=[Depends(get_current_user)])


@router.post(
    "/create",
    response_model=ConsoleWithOwner,
    status_code=201
)
def create_console(
        current_user: Annotated[User, Depends(get_current_user)],
        db: Session = Depends(get_db),
):

    last_console = db.query(Console).order_by(Console.id.desc()).first()
    next_number = 1 if not last_console else last_console.id + 1

    new_console = Console(
        name=str(next_number),
        owner=current_user
    )

    db.add(new_console)
    db.commit()
    db.refresh(new_console)

    return new_console


@router.get("/list", response_model=list[ConsoleWithOwner])
def get_all_consoles(db: Session = Depends(get_db)):
    consoles = db.query(Console).all()
    return consoles
