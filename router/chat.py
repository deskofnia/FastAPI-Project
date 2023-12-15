from fastapi import APIRouter, Depends, Request, Response, WebSocket
from oauth2 import get_token
from repository.chat import token_generator, websocket_endpoint
from schemas.chat_schemas import RegisterValidator


router = APIRouter(tags=["CHAT"], prefix="/message")


# Token Generation API
@router.post("/token")
async def token_route(name:str, request: Request):
    return await token_generator(name, request)

# Chat API
@router.websocket("/ws")
async def chat_route(websocket:WebSocket):
    return await websocket_endpoint(websocket)
