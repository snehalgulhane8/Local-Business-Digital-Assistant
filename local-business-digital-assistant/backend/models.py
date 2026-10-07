from pydantic import BaseModel

class BusinessQuestion(BaseModel):
    question: str
