from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from oauth2 import get_current_user
from repository.question import get_questions
from schemas.user_schemas import ResponseModal

router = APIRouter(tags=["QUESTION"], prefix="/questions")
print(">>>>>>>????")
# Get All Questions API
@router.get("/", response_model=ResponseModal)
def get_questions_route( db: Session = Depends(get_db), user_info: Session=Depends(get_current_user) ):
    return get_questions(db)