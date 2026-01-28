from app.core.security import get_current_user
from fastapi import APIRouter, Depends
from app.schemas.user import UserOut
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User

router = APIRouter(prefix="/api/v1/user", tags=["User"], dependencies=[Depends(get_current_user)])


@router.get("/list", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
