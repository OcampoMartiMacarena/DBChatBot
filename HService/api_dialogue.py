from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from HService.domain.dialogue_manager import DialogueManager, Message

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
        # Convert ChatHistoryModel to List[Message]
        messages = [Message(role=msg.sender, content=msg.msg) for msg in chat_history.chat_history]
        
        # Get response from DialogueManager
        response = dialogue_manager.get_response(messages)
        
        return BotResponse(response=response.bot_msg, is_ticket_closed=response.is_ticket_closed)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
