from pymongo import MongoClient
import os
from dotenv import load_dotenv


load_dotenv()          # <-- this reads your .env file

client = MongoClient(os.getenv("MONGODB_URI"))
db = client["chatbot_db"]

user_collection = db["users"]
chat_collection = db["chats"]


def find_chat_object(username):
    if chat_collection.find_one({"username": username}):
        return True
    return False

def create_chat_object(username):
    msg=[{"role": "system", "content": "You are a helpful assistant."}]
    try:
        chat_collection.insert_one({"username": username, "messages": msg})
        return True
    except Exception as e:
        print(f"Error creating chat object for {username}: {e}")
    
    return False

def get_chat_history(username):
    chat = chat_collection.find_one({"username": username})
    if chat:
        return chat.get("messages", [])
    return []

def update_chat_history(username, messages):
    try:
        chat_collection.update_one(
            {"username": username},
            {"$set": {"messages": messages}}
        )
        return True
    except Exception as e:
        print(f"Error updating chat history for {username}: {e}")   
        return False
