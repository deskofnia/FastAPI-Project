from datetime import datetime
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, HTTPException, status, WebSocket, status, Query
from jose import JWTError, jwt
from pydantic import ValidationError
from typing import Optional
from config import env_variables

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),  
):  
    try:
        token = credentials.credentials
        payload = jwt.decode(
            token, env_variables.SECRET_KEY, algorithms=[env_variables.ALGORITHM]
        )
        user_id = payload.get("id")
        email = payload.get("email")
        print(">>>>user", payload["id"], ">>>>email", email, ">>>token" )

        # if datetime.fromtimestamp( payload.get("exp")) > datetime.now():
        #     raise HTTPException(
        #         status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        #     )
        if not user_id or not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        # You can perform additional checks or fetch the user from the database based on user_id and email
        # For demonstration purposes, we'll return the user_id and email
        return {"user_id": user_id, "email": email}
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

async def check_token_middleware(user: dict = Depends(get_current_user)):
    # Here you can perform additional checks or actions based on the user information
    # For example, you can log the user details or perform authorization checks
    print(f"Authenticated User: {user['user_id']}, Email: {user['email']}")
    return


async def get_token(
    websocket: WebSocket,
    token: Optional[str] = Query(None),
):
    if token is None or token == "":
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)

    return token