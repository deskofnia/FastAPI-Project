from fastapi import FastAPI, APIRouter, status
from fastapi.middleware.cors import CORSMiddleware
from router import (chat, note, auth, question)
from database import engine, Base

Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

routes = APIRouter()

routes.include_router(note.router)
routes.include_router(auth.router)
routes.include_router(chat.router)
routes.include_router(question.router)


app.include_router(routes, prefix="/api/v1")
