from fastapi import FastAPI
from pydantic import BaseModel
from src.brain import process_query

app = FastAPI()

class Query(BaseModel):
    question: str
    mode: str = "full"

@app.get("/")
def root():
    return {"status": "JARVIS Core Online"}

@app.post("/ask")
def ask(q: Query):
    response = process_query(q.question, q.mode)
    return {"response": response}
