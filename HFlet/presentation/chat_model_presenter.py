from enum import Enum, auto
from pydantic import BaseModel, Field
from typing import Protocol, List, Callable
import sys
import os
import requests

# Add the parent directory to the path so we can import from HService
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import from HService
from HService.domain.dialogue_manager import Message, Response, Intent

import flet as ft

class ViewProtocol(Protocol):
    def get_user_message(self) -> str: ...
    def display_bot_message(self, message: str) -> None: ...
    def display_user_message(self, message: str) -> None: ...
    def clear_user_input(self) -> None: ...
    def show_loading_indicator(self) -> None: ...
    def hide_loading_indicator(self) -> None: ...

class BotResponse(BaseModel):
    msg: str
    is_ticket_closed: bool

class ChatModel(BaseModel):
    conversation_history: List[dict] = Field(default_factory=list)

class ChatPresenter:
    def __init__(self, view: ViewProtocol, page: ft.Page):
        self.model = ChatModel()
        self.view = view
        self.page = page
        self.api_url = "http://localhost:8000"
        self.conversation_history = []
        self.bot_msg = ""
        self.is_ticket_closed = False

    def clear_chat_history(self):
        self.model.conversation_history.clear()
        self.conversation_history = []
        self.bot_msg = ""
        self.is_ticket_closed = False

    def process_user_message(self, message):
        # Display user message
        self.view.display_user_message(message)

        # Show loading indicator
        self.view.show_loading_indicator()

        # Add user message to conversation history
        self.model.conversation_history.append({"role": "user", "content": message})
        self.conversation_history.append({"role": "user", "content": message})

        # Generate bot response using HService API
        try:
            # Call the API
            response = requests.post(
                f"{self.api_url}/chat",
                json={"chat_history": [{"sender": msg["role"], "msg": msg["content"]} for msg in self.conversation_history]}
            )
            
            if response.status_code == 200:
                result = response.json()
                self.bot_msg = result["response"]
                self.is_ticket_closed = result["is_ticket_closed"]
            else:
                error_msg = f"API error: {response.status_code} - {response.text}"
                self.bot_msg = error_msg
                self.is_ticket_closed = False
        except Exception as e:
            error_msg = f"Error connecting to API: {str(e)}"
            self.bot_msg = error_msg
            self.is_ticket_closed = False

        # Hide loading indicator
        self.view.hide_loading_indicator()

        # Display bot response
        self.view.display_bot_message(self.bot_msg)

        # Add bot response to conversation history
        self.model.conversation_history.append({"role": "assistant", "content": self.bot_msg})
        self.conversation_history.append({"role": "assistant", "content": self.bot_msg})

        # Clear user input
        self.view.clear_user_input()

        # If the ticket is closed, you might want to handle it here
        if self.is_ticket_closed:
            self.view.display_bot_message("The support ticket has been closed. Thank you for using our service!")

    def get_chat_history(self):
        return self.conversation_history

    def print_chat_history(self):
        print("\nChat History:")
        for message in self.conversation_history:
            print(f"{message['role']}: {message['content']}")

    def handle_send(self, message):
        self.process_user_message(message)

    def set_on_send_handler(self, chat_view):
        chat_view.on_send = self.handle_send

    def new_ticket(self):
        # Clear the chat history
        self.clear_chat_history()

        # Display a message indicating a new chat has started
        new_chat_message = "A new support ticket has been opened. How can I assist you today?"
        self.view.display_bot_message(new_chat_message)

        # Add the new chat message to the conversation history
        self.model.conversation_history.append({"role": "assistant", "content": new_chat_message})
        self.conversation_history.append({"role": "assistant", "content": new_chat_message})
