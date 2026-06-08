from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from llm import get_response
from auth import authenticate_user, register_user
from db import get_chat_history

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

#  Home redirect
@app.get("/", response_class=HTMLResponse)
def home():
    return RedirectResponse(url="/login")

#  Register Page
@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(request=request, name="register.html")

@app.post("/register")
def register_user_endpoint(username: str = Form(...), password: str = Form(...)):
    is_registered, message = register_user(username, password)

    if not is_registered:
        return JSONResponse(status_code=400, content={"error": f"{message}"})

    response = RedirectResponse(url="/login", status_code=302)
    return response


#  Login Page
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

# Profile Page
@app.get("/profile", response_class=HTMLResponse)
def profile_page(request: Request):
    username = request.cookies.get("user")
    if not username:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse(request=request, name="profile.html")

@app.post("/login")
def login_user(username: str = Form(...), password: str = Form(...)):
    is_authenticated, message = authenticate_user(username, password)

    if not is_authenticated:
        return JSONResponse(status_code=400, content={"error": f"{message}"})

    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(key="user", value=username)
    return response

@app.get("/logout")
def logout_user():
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie(key="user")
    return response

@app.get("/dashboard", response_class=HTMLResponse)
def home(request: Request):
    token = request.cookies.get("user")
    if not token:
        return RedirectResponse(url="/login")
    
    return templates.TemplateResponse(request=request, name="dashboard.html")

# Request body schema
class ChatRequest(BaseModel):
    message: str

# API endpoint
@app.post("/chat")
def chat(request: Request,body:ChatRequest):
    user_message = body.message
    username = request.cookies.get("user")
    
    response = get_response(username,user_message)

    return {
        "user": user_message,
        "response": response
    }

@app.get("/chat_history")
def chat_history(request: Request):
    username = request.cookies.get("user")
    history = get_chat_history(username)
    
    return {"history": history}