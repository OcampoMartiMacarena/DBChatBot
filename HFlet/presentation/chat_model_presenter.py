from pydantic import BaseModel, Field
from typing import Protocol, List

class ViewProtocol(Protocol):
    def get_user_message(self) -> str: ...
    def display_bot_message(self, message: str) -> None: ...
    def clear_user_input(self) -> None: ...
    def show_loading_indicator(self) -> None: ...
    def hide_loading_indicator(self) -> None: ...

class ChatModel(BaseModel):
    conversation_history: List[dict] = Field(default_factory=list)

class ChatPresenter:
    def __init__(self, view: ViewProtocol):
        self.model = ChatModel()
        self.view = view

    def start_chat(self):
        welcome_message = "Hello! I'm your AI assistant. How can I help you today?"
        self.view.display_bot_message(welcome_message)
        self.model.conversation_history.append({"role": "assistant", "content": welcome_message})

    def clear_chat_history(self):
        self.model.conversation_history.clear()
        self.start_chat()

    def process_user_message(self, message):
        # Process the user message here
        # For example, you might want to send it to an AI model or perform some other operation
        print(f"Processing user message: {message}")
        
        # After processing, you might want to update the view
        # self.view.update_view(some_data)
