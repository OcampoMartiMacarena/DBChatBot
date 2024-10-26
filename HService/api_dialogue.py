from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from domain.dialogue_manager import DialogueManager, Message

app = FastAPI()

class MessageModel(BaseModel):
    sender: str
    msg: str

class ChatHistoryModel(BaseModel):
    chat_history: List[MessageModel]

class BotResponse(BaseModel):
    response: str
    is_ticket_closed: bool

dialogue_manager = DialogueManager()

@app.post("/chat", response_model=BotResponse)
async def chat(chat_history: ChatHistoryModel):
    try:
        response = "This is a dummy response from the server."
        is_ticket_closed = False

        return BotResponse(response=response, is_ticket_closed=is_ticket_closed)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
