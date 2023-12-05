import database
from fastapi import APIRouter, Depends
from repository.auth import (login, signup, get_users)
from sqlalchemy.orm import Session
from schemas.user_schemas import LoginSchema, ResponseModal, UserSchema


get_db = database.get_db

router = APIRouter(tags=["AUTH"], prefix="/auth")


# Get Users API
@router.get("/", response_model=ResponseModal)
def get_users_route(db: Session = Depends(get_db)):
    return get_users(db)

# SIGNUP API
@router.post("/signup", response_model=ResponseModal)
def signup_route(request: UserSchema, db: Session = Depends(get_db)):
    return signup(request, db)


# LOGIN API
@router.post("/login", response_model=ResponseModal)
def login_route(request: LoginSchema, db: Session = Depends(database.get_db)):
    return login(request, db)


# # FORGOT PASSWORD API
# @router.post("/forgot-password", response_model=ResponseModal)
# def forgot_password_route(request: ForgotPassSchema, db: Session = Depends(database.get_db)):
#     return forgot_password(request, db)


# # VERIFY PASSWORD API
# @router.post("/verify-otp", response_model=ResponseModal)
# def verify_otp_route(request: VerifyOtpSchema, db: Session = Depends(database.get_db)):
#     return verify_otp(request, db)


# # RESET PASSWORD API
# @router.post("/reset-password", response_model=ResponseModal)
# def reset_password_route(
#     reset_form: ResetPasswordFormSchema, db: Session = Depends(database.get_db)
# ):
#     return reset_password(reset_form, db)


# # VERIFY SIGNUP OTP API
# @router.post("/verify-signup-otp", response_model=ResponseModal)
# def verify_signup_otp_route(
#     request: VerifyUserSignupOtpSchema, db: Session = Depends(database.get_db)
# ):
#     return verify_signup_otp(request, db)


# # RESEND OTP API
# @router.post("/resend-otp", response_model=ResponseModal)
# def resend_otp_route(request: ResendOtpSchema, db: Session = Depends(database.get_db)):
#     return resend_otp(request, db)

