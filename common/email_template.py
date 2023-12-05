from common.sendgrid_utils import send_email
from config import env_variables

def send_verify_otp_email(user_email, otp, mailType):
    subject = ""
    if mailType == "forgotPassword":
        subject = "Forgot password otp"
    elif mailType == "login":
        subject = "Login otp"
    else:
        subject = "Sign up otp"
    send_email(env_variables.SENDGRID_ADMIN_MAIL, user_email, subject, f"Your OTP code is - {otp}")
