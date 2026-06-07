from pymongo import MongoClient
import os
from dotenv import load_dotenv


load_dotenv()          # <-- this reads your .env file

client = MongoClient(os.getenv("MONGODB_URI"))
db = client["chatbot_db"]

user_collection = db["users"]
chat_collection = db["chats"]
