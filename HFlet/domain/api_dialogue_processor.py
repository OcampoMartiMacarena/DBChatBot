import sys
from pathlib import Path
import requests
from pydantic import BaseModel, Field
from typing import List

# Add the project root to the Python path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

from .mock_dialogue_processor import ChatHistoryManager

class MessageModel(BaseModel):
    sender: str
    msg: str

class ChatHistoryModel(BaseModel):
    chat_history: List[MessageModel] = Field(default_factory=list)

class BotResponse(BaseModel):
    response: str
    is_ticket_closed: bool

class APIDialogueProcessor:
    def __init__(self):
        self.api_base_url = "http://localhost:8000"  # Adjust this to your API server's address

    def generate_response(self, chat_manager: ChatHistoryManager) -> None:
        """
        Generates a response based on the chat history using the API server.
        """
        if not chat_manager.chat_history:
            return

        try:
            # Convert chat_history to a list of MessageModel
            chat_history = [MessageModel(sender=msg.sender, msg=msg.msg) for msg in chat_manager.chat_history]
            
            payload = ChatHistoryModel(chat_history=chat_history).model_dump()
            response = requests.post(f"{self.api_base_url}/chat", json=payload)
            
            response.raise_for_status()
            data = response.json()
            
            bot_response = BotResponse(**data)
            chat_manager.set_bot_response(bot_response.response, bot_response.is_ticket_closed)
        except Exception as e:
            error_message = f"An error occurred while communicating with the API: {str(e)}"
            chat_manager.set_bot_response(error_message, False)

# Example usage
if __name__ == "__main__":
    processor = APIDialogueProcessor()
    chat_manager = ChatHistoryManager()
    
    # Get user input
    user_input = input("Enter your message: ")
    
    chat_manager.add_message("user", user_input)
    processor.generate_response(chat_manager)
    
    print("Bot response:")
    print(chat_manager.bot_msg)
    print("Is ticket closed:", chat_manager.is_ticket_closed)
