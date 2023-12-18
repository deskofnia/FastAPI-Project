from requests import Session
from models.question import Question


# Get Questions
def get_questions(db: Session):
    questions = db.query(Question).all()
    return {"success": True, "message": "questions_list_fetched", "data": questions}