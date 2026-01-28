from typing import Annotated

from app.schemas.console import ConsoleWithUser, ConsoleCreate
from app.core.security import get_current_user
from fastapi import APIRouter, Depends
from app.models.console import Console
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User

router = APIRouter(prefix="/api/v1/console", tags=["Console"], dependencies=[Depends(get_current_user)])


@router.post(
    "/create",
    response_model=ConsoleWithUser,
    status_code=201
)
def create_console(
        current_user: Annotated[User, Depends(get_current_user)],
        console: ConsoleCreate,
        db: Session = Depends(get_db),
):
    new_console = Console(
        name=console.name,
        owner=current_user
    )

    db.add(new_console)
    db.commit()
    db.refresh(new_console)

    return new_console


@router.get("/list", response_model=list[ConsoleWithUser])
def get_all_consoles(db: Session = Depends(get_db)):
    consoles = db.query(Console).all()
    return consoles
