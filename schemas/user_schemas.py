from pydantic import BaseModel, EmailStr, Field
from typing import Any


class ResponseModal(BaseModel):
    message: str
    success: bool
    data: Any | None = None


password_regex = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])(?!.*\s).{8,16}$"
phone_regex = r"^\+1\d{10}$"


class TokenData(BaseModel):
    email: str | None = None
    user_id: int | None = None


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class ForgotPassSchema(BaseModel):
    email: EmailStr


class UserSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., regex=password_regex)
    is_admin: bool | None = None