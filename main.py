from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from llm import get_response

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

# Request body schema
class ChatRequest(BaseModel):
    message: str

# API endpoint
@app.post("/chat")
def chat(request: ChatRequest):
    user_message = request.message

    response = get_response(user_message)

    return {
        "user": user_message,
        "response": response
    }