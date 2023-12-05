import base64
from datetime import datetime, timedelta
import json
import random
import string
from config import env_variables
from jose import jwt
from passlib.hash import pbkdf2_sha256
from cryptography.fernet import Fernet, InvalidToken


# Generate a random OTP
def generate_otp(length=6):
    characters = string.digits
    otp = "".join(random.choice(characters) for _ in range(length))
    return otp

# Create access token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=int(env_variables.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, env_variables.SECRET_KEY, algorithm=env_variables.ALGORITHM
    )
    return encoded_jwt

# Verify password
def verify_password(plain_password, hashed_password):
    return pbkdf2_sha256.verify(plain_password, hashed_password)

# Encrypt OTP
def encrypt_otp(otp: int) -> str:
    key = env_variables.ENCRYPTION_KEY
    if key is None:
        raise ValueError("Encryption key not found in environment variable.")
    f = Fernet(key.encode())
    encrypted_otp = f.encrypt(str(otp).encode())
    encoded_otp = base64.urlsafe_b64encode(encrypted_otp).decode()
    return encoded_otp

# Decrypt OTP
def decrypt_otp(encrypted_otp: str) -> str:
    key = env_variables.ENCRYPTION_KEY

    if key is None:
        raise ValueError("Encryption key not found in environment variable.")

    if len(key) != 32:
        raise ValueError("Invalid Fernet key. Key must be 32 bytes.")

    try:
        f = Fernet(key.encode())
        decrypted_otp = f.decrypt(base64.urlsafe_b64decode(encrypted_otp.encode()))
        return decrypted_otp.decode()
    except InvalidToken:
        raise ValueError("Invalid or corrupted ciphertext.")
    
def encrypt_json(json_data: dict) -> str:
    key = env_variables.ENCRYPTION_KEY
    if key is None:
        raise ValueError("Encryption key not found in environment variable.")
    f = Fernet(key.encode())
    encrypted_data = f.encrypt(json.dumps(json_data).encode())
    encoded_data = base64.urlsafe_b64encode(encrypted_data).decode()
    return encoded_data


def decrypt_json(encoded_data: str) -> dict:
    key = env_variables.ENCRYPTION_KEY
    if key is None:
        raise ValueError("Encryption key not found in environment variable.")
    f = Fernet(key.encode())
    try:
        decoded_data = base64.urlsafe_b64decode(encoded_data.encode())
        decrypted_data = f.decrypt(decoded_data).decode()
        json_data = json.loads(decrypted_data)
        return json_data
    except (json.JSONDecodeError, InvalidToken, ValueError):
        return {}