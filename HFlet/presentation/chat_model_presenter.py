from pydantic import BaseModel, Field
from typing import Protocol, List
from domain.mock_dialogue_processor import MockDialogueProcessor, Message

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
    def __init__(self, view: ViewProtocol):
        self.model = ChatModel()
        self.view = view
        self.dialogue_processor = MockDialogueProcessor()

    def start_chat(self):
        welcome_message = "Hello! I'm your AI assistant. How can I help you today?"
        self.view.display_bot_message(welcome_message)
        self.model.conversation_history.append({"role": "assistant", "content": welcome_message})

    def clear_chat_history(self):
        self.model.conversation_history.clear()
        self.start_chat()

    def process_user_message(self, message):
        # Display user message
        self.view.display_user_message(message)

        # Show loading indicator
        self.view.show_loading_indicator()

        # Add user message to conversation history
        self.model.conversation_history.append({"role": "user", "content": message})

        # Convert conversation history to List[Message]
        chat_history = [Message(msg["role"], msg["content"]) for msg in self.model.conversation_history]

        # Generate bot response using MockDialogueProcessor
        bot_response, is_ticket_closed = self.dialogue_processor.generate_response(chat_history)

        # Hide loading indicator
        self.view.hide_loading_indicator()

        # Display bot response
        self.view.display_bot_message(bot_response)

        # Add bot response to conversation history
        self.model.conversation_history.append({"role": "assistant", "content": bot_response})

        # Clear user input
        self.view.clear_user_input()

        # If the ticket is closed, you might want to handle it here
        if is_ticket_closed:
            self.view.display_bot_message("The support ticket has been closed. Thank you for using our service!")
