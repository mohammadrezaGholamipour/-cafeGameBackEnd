from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.auth import LoginRequest, TokenResponse
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserCreate, UserOut
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


# ===================== REGISTER =====================
@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # بررسی ایمیل
    if user.email:
        existing_email = (
            db.query(User)
            .filter(User.email == user.email)
            .first()
        )
        if existing_email:
            raise HTTPException(
                status_code=400,
                detail={
                    "field": "email",
                    "message": "این ایمیل قبلاً ثبت شده است"
                }
            )

    # بررسی موبایل
    if user.mobile:
        existing_mobile = (
            db.query(User)
            .filter(User.mobile == user.mobile)
            .first()
        )
        if existing_mobile:
            raise HTTPException(
                status_code=400,
                detail={
                    "field": "mobile",
                    "message": "این شماره موبایل قبلاً ثبت شده است"
                }
            )

    new_user = User(
        userName=user.userName,
        email=user.email,
        mobile=user.mobile,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ===================== LOGIN =====================
@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=400,
            detail={
                "field": "email",
                "message": "کاربری با این ایمیل یافت نشد"
            }
        )

    if not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=400,
            detail={
                "field": "password",
                "message": "رمز عبور نادرست است"
            }
        )

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
