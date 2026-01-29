from pydantic import BaseModel, field_validator, FieldValidationInfo

from pydantic_core import PydanticCustomError
import re


class UserCreate(BaseModel):
    email: str
    mobile: str
    userName: str
    password: str
    repeatPassword: str

    @field_validator("email")
    @classmethod
    def valid_email(cls, v):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(pattern, v):
            raise PydanticCustomError("email", "ایمیل وارد شده معتبر نمی‌باشد")
        return v

    @field_validator("userName")
    @classmethod
    def username_length(cls, v):
        if len(v) < 3:
            raise PydanticCustomError("userName", "نام و نام خانوادگی حداقل باید ۳ حرف باشد")
        return v

    @field_validator("mobile")
    @classmethod
    def valid_mobile(cls, v):
        pattern = r"^09\d{9}$"
        if not re.match(pattern, v):
            raise PydanticCustomError("mobile", "شماره موبایل وارد شده معتبر نمیباشد")
        return v

    @field_validator("password")
    @classmethod
    def strong_password(cls, v):
        if len(v) < 6:
            raise PydanticCustomError("password", "رمز عبور حداقل باید ۶ اجزا داشته باشد")
        if not re.search(r"[A-Za-z]", v):
            raise PydanticCustomError("password", "رمز عبور باید شامل حروف باشد")
        if not re.search(r"\d", v):
            raise PydanticCustomError("password", "رمز عبور باید شامل اعداد باشد")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise PydanticCustomError("password", "رمز عبور باید شامل کاراکتر باشد")
        return v

    @field_validator("repeatPassword")
    @classmethod
    def passwords_match(cls, v, info: FieldValidationInfo):
        password = info.data.get("password")
        if password and v != password:
            raise PydanticCustomError("repeatPassword", "رمز عبور تکرار شده صحیح نمیباشد")
        return v


class UserOut(BaseModel):
    id: int
    userName: str
    email: str
    mobile: str
    unitPrice: list["UnitPriceWithOutUser"]
    consoles: list["ConsoleWithOutUser"]
    buffet: list["BuffetWithOutOwner"]
    model_config = {
        "from_attributes": True
    }


class UserWithOutDetails(BaseModel):
    id: int
    userName: str
    email: str
    mobile: str
    model_config = {
        "from_attributes": True
    }


from app.schemas.unitPrice import UnitPriceWithOutUser
from app.schemas.console import ConsoleWithOutUser
from app.schemas.buffet import BuffetWithOutOwner

UnitPriceWithOutUser.model_rebuild()
ConsoleWithOutUser.model_rebuild()
BuffetWithOutOwner.model_rebuild()
