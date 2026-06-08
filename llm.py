import os
from openai import OpenAI
from dotenv import load_dotenv
from db import find_chat_object, create_chat_object,get_chat_history,update_chat_history


load_dotenv()          # <-- this reads your .env file
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

def get_response(username, prompt):
    if not find_chat_object(username):
        create_chat_object(username)

    messages = get_chat_history(username)
    messages.append({"role": "user", "content": prompt})
    print("messages", messages)
    #update_chat_history(username, messages)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )
    print("response", response)
    messages.append({"role": "assistant", "content": response.choices[0].message.content})
    update_chat_history(username, messages)

    return response.choices[0].message.content
    