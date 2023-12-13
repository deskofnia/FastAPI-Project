from fastapi import APIRouter, Depends, Request, Response, WebSocket
from oauth2 import get_token
from repository.chat import get_home_html, get_chat_html, token_generator, websocket_endpoint
from schemas.chat_schemas import RegisterValidator


router = APIRouter(tags=["CHAT"], prefix="/message")

# Get Chat HTML API
@router.get("/chat")
async def get_html_route():
    return await get_chat_html()

# Get Home HTML API
@router.get("/")
async def get_html_route():
    return await get_home_html()

# Token Generation API
@router.post("/token")
async def token_route(name:str, request: Request):
    return await token_generator(name, request)

# Refresh Token API
@router.post("/refresh_token")
async def refresh_token_route(request: Request):
    return None

# Chat API
@router.websocket("/ws")
async def chat_route(websocket:WebSocket):
    return await websocket_endpoint(websocket)

# Get Current Logged In User API
@router.get("/current_user")
async def current_user_route(request: Request):
    return await request.cookies.get("X-Authorization")

# Register User API
@router.post("/register")
async def register_route(user: RegisterValidator, response: Response):
    response.set_cookie(key="X-Authorization", value=user.username, httponly=True)