from common.email_template import send_verify_otp_email
from schemas.user_schemas import ForgotPassSchema, LoginSchema, UserSchema
from sqlalchemy.orm import Session
from passlib.hash import pbkdf2_sha256
from models.user import (User, UserStatus)
from common.utils import (
    create_access_token,
    decrypt_otp,
    encrypt_otp,
    generate_otp,
    verify_password,
)

# Get Users
def get_users(db: Session):
    users = db.query(User).all()
    return {"success": True, "message": "user_list_fetched", "data": users}
    
# SignUp API
def signup(request: UserSchema, db: Session):
    try:
        existing_user = db.query(User).filter(User.email == request.email).first()
        if existing_user:
            return {"message": "user_with_email_already_exists", "success": False}
        
        otp = generate_otp()
        password_hash = pbkdf2_sha256.hash(request.password)

        new_user = User(
            email=request.email,
            is_admin=request.is_admin,
            password=password_hash,
        )

        # send_verify_otp_email(request.email, otp, "signup")
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        # token_handling_result = False
        # if request.token:
        #     token_handling_result = handle_token(request, new_user, db)

        # user = db.query(User).filter(User.email == request.email).first()
        # encrypted_id = encrypt_otp(user.id)


        return {
            "message": "signup_successfully",
            "success": True,
            # "data": {"encrypted_id": encrypted_id} 
        }
    except Exception as e:
        raise e
    
# Login API
def login(request: LoginSchema, db: Session):
    try:
        user = db.query(User).filter(User.email == request.email).first()

        if not user:
            return {"message": "email_not_exist", "success": False}
        
        if user.is_active == 2:
            return {"message": "you_are_blocked", "success": False}
        
        if not user.is_active:
            return {"message": "user_inactive", "success": False}
        
        if not verify_password(request.password, user.password):
            return {"message": "incorrect_password", "success": False}
        
        else:
            access_token = create_access_token({"email": user.email, "id": user.id})

            return {
                "message": "login_successfully",
                "success": True,
                "data": {"token":access_token},
            }
    except Exception as e:
        raise e

# # Forgot Password API
# def forgot_password(request: ForgotPassSchema, db: Session):
#     try:
#         global otp
#         user_exists = db.query(User).filter(User.email == request.email).first()

#         if not user_exists:
#             return {"message": "user_not_found", "success": False}
#         otp = generate_otp()
#         user_exists.verification_otp = otp
#         db.commit()
#         encrypted_id = encrypt_otp(user_exists.id)
#         send_verify_otp_email(request.email, otp, "forgotPassword")

#         return {
#             "data": {
#                 "encrypted_id": encrypted_id,
#                 "user_email": request.email,
#             },
#             "message": "otp_has_been_sent_successfully",
#             "success": True,
#         }
#     except Exception as e:
#         raise e

# # Verify OTP API
# def verify_otp(request, db: Session):
#     try:
#         decrypted_otp = decrypt_otp(request.encrypted_otp)
#         if request.user_otp == decrypted_otp:
#             return {
#                 "message": "otp_verified_successfully",
#                 "success": True,
#                 "data": {"email": request.email},
#             }
#         else:
#             return {"message": "invalid_otp", "success": False}

#     except Exception as e:
#         raise e


# # Reset Password API
# def reset_password(request, db: Session):
#     try:
#         enc_id = request.enc_id
#         new_password = request.new_password
#         decrypted_id = decrypt_otp(enc_id)

#         user = db.query(User).filter(User.id == decrypted_id).first()

#         if not user:
#             return {"message": "user_not_found", "success": False}

#         hashed_password = pbkdf2_sha256.hash(new_password)
#         user.password = (
#             hashed_password  # Update the password attribute of the user instance
#         )
#         db.commit()

#         return {"message": "password_reset_successfully", "success": True}
    
#     except Exception as e:
#         raise e
    
# # Verify SignUp OTP API
# def verify_signup_otp(request, db: Session):
#     try:
#         enter_otp = request.enter_otp
#         enc_id = request.enc_id
#         decrypted_id = decrypt_otp(enc_id)
#         userInfo = db.query(User).filter(User.id == decrypted_id).first()

#         if userInfo.verification_otp == enter_otp:
#             if request.page == "signup" or request.page == "login":
#                 userInfo.is_active = UserStatus.Active
#             userInfo.verification_otp = None
#             db.commit()
#         else:
#             return {"message": "otp_verify_failed", "success": False}

#         return {"message": "otp_verified_successfully", "success": True}
#     except Exception as e:
#         raise e

# # Resend OTP API
# def resend_otp(request, db: Session):
#     try:
#         global otp
#         enc_id = request.enc_id
#         decrypted_id = decrypt_otp(enc_id)
#         userInfo = db.query(User).filter(User.id == decrypted_id).first()
#         if not userInfo:
#             return {"message": "user_not_found", "success": False}
#         otp = generate_otp()
#         userInfo.verification_otp = otp
#         db.commit()
#         encrypted_id = encrypt_otp(userInfo.id)
#         emailres = send_verify_otp_email(userInfo.email, otp, request.otp_type)

#         return {
#             "message": "otp_has_been_sent_successfully",
#             "success": True,
#             "data": {
#                 "encrypted_id": encrypted_id,
#                 "user_email": userInfo.email,
#             },
#         }
#     except Exception as e:
#         raise e