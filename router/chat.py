from fastapi import APIRouter, Depends, Request, WebSocket
from oauth2 import get_token

from repository.chat import get_html, token_generator, websocket_endpoint


router = APIRouter(tags=["CHAT"], prefix="/message")

# Get HTML API
@router.get("/")
async def get_html_route():
    return await get_html()

# Token Generation API
@router.post("/token")
async def token_route(name:str, request: Request):
    return await token_generator(name, request)

# Refresh Token API
@router.post("/refresh_token")
async def token_route(request: Request):
    return None

# Chat API
@router.websocket("/chat")
async def chat_route(websocket:WebSocket):
    return await websocket_endpoint(websocket)
