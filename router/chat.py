from fastapi import APIRouter
from repository.chat import chat


router = APIRouter(tags=["AUTH"], prefix="/chat")

# Chat API
@router.post("/chat")
def chat_route(message:str):
    return chat(message)

