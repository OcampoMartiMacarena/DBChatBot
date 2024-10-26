from enum import Enum, auto
from pydantic import BaseModel, Field
from typing import Protocol, List, Callable
from domain.api_dialogue_processor import APIDialogueProcessor, ChatHistoryManager
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

class Intent(Enum):
    # ACCOUNT
    CREATE_ACCOUNT = auto()
    DELETE_ACCOUNT = auto()
    EDIT_ACCOUNT = auto()
    SWITCH_ACCOUNT = auto()

    # CANCELLATION_FEE
    CHECK_CANCELLATION_FEE = auto()

    # DELIVERY
    DELIVERY_OPTIONS = auto()

    # FEEDBACK
    COMPLAINT = auto()
    REVIEW = auto()

    # INVOICE
    CHECK_INVOICE = auto()
    GET_INVOICE = auto()

    # NEWSLETTER
    NEWSLETTER_SUBSCRIPTION = auto()

    # ORDER
    CANCEL_ORDER = auto()
    CHANGE_ORDER = auto()
    PLACE_ORDER = auto()

    # PAYMENT
    CHECK_PAYMENT_METHODS = auto()
    PAYMENT_ISSUE = auto()

    # REFUND
    CHECK_REFUND_POLICY = auto()
    TRACK_REFUND = auto()

    # SHIPPING_ADDRESS
    CHANGE_SHIPPING_ADDRESS = auto()
    SET_UP_SHIPPING_ADDRESS = auto()

class ChatPresenter:
    def __init__(self, view: ViewProtocol, page: ft.Page):
        self.model = ChatModel()
        self.view = view
        self.page = page
        self.dialogue_processor = APIDialogueProcessor()
        self.chat_history_manager = ChatHistoryManager()

    

    def clear_chat_history(self):
        self.model.conversation_history.clear()
        

    def process_user_message(self, message):
        # Display user message
        self.view.display_user_message(message)

        # Show loading indicator
        self.view.show_loading_indicator()

        # Add user message to conversation history
        self.model.conversation_history.append({"role": "user", "content": message})

        # Add user message to chat history manager
        self.chat_history_manager.add_message("user", message)

        # Generate bot response using APIDialogueProcessor
        self.dialogue_processor.generate_response(self.chat_history_manager)

        # Get the bot response from the chat history manager
        bot_response = self.chat_history_manager.bot_msg
        is_ticket_closed = self.chat_history_manager.is_ticket_closed

        # Hide loading indicator
        self.view.hide_loading_indicator()

        # Display bot response
        self.view.display_bot_message(bot_response)

        # Add bot response to conversation history
        self.model.conversation_history.append({"role": "assistant", "content": bot_response})

        # Save the bot message to the chat history manager
        self.chat_history_manager.save_last_message()

        # Clear user input
        self.view.clear_user_input()

        # If the ticket is closed, you might want to handle it here
        if is_ticket_closed:
            self.view.display_bot_message("The support ticket has been closed. Thank you for using our service!")

    def get_chat_history(self):
        return self.chat_history_manager.chat_history

    def print_chat_history(self):
        print("\nChat History:")
        for message in self.chat_history_manager.chat_history:
            print(f"{message.sender}: {message.msg}")

    def handle_send(self, message):
        self.process_user_message(message)

    def set_on_send_handler(self, chat_view):
        chat_view.on_send = self.handle_send

    def new_ticket(self):
        # Clear the chat history
        self.clear_chat_history()
        self.chat_history_manager.clear_history()

        # Display a message indicating a new chat has started
        new_chat_message = "A new support ticket has been opened. How can I assist you today?"
        self.view.display_bot_message(new_chat_message)

        # Add the new chat message to the conversation history and chat history manager
        self.model.conversation_history.append({"role": "assistant", "content": new_chat_message})
        self.chat_history_manager.add_message("assistant", new_chat_message)
