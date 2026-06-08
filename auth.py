from db import user_collection
import hashlib
from db import create_user,find_user,update_login_status

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    hashed_password = hash_password(password)
    status, message = create_user(username, hashed_password)
    return status, message

def authenticate_user(username, password):
    user = find_user(username)
    if not user:
        return False, "User not found."
    
    if user.get("login", False):
        return False, "User already logged in."

    hashed_password = hash_password(password)
    if user["password"] != hashed_password:
        return False, "Incorrect password."
    
    login_status, message = update_login_status(username)

    return login_status, message

