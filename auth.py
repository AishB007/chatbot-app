from db import user_collection
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    if user_collection.find_one({"username": username}):
        return False, "Username already exists."

    hashed_password = hash_password(password)
    user_collection.insert_one({"username": username, "password": hashed_password})
    return True, "User registered successfully."

def authenticate_user(username, password):
    user = user_collection.find_one({"username": username})
    if not user:
        return False, "User not found."

    hashed_password = hash_password(password)
    if user["password"] != hashed_password:
        return False, "Incorrect password."

    return True, "Authentication successful."

