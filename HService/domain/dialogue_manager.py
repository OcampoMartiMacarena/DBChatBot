from pydantic import BaseModel
from typing import List
from enum import Enum, auto

class IntentCategory(Enum):
    ACCOUNT = auto()
    CANCELLATION_FEE = auto()
    DELIVERY = auto()
    FEEDBACK = auto()
    INVOICE = auto()
    NEWSLETTER = auto()
    ORDER = auto()
    PAYMENT = auto()
    REFUND = auto()
    SHIPPING_ADDRESS = auto()


class Message(BaseModel):
    role: str
    content: str

class Response(BaseModel):
    intent_category: IntentCategory
    bot_msg: str
    is_ticket_closed: bool

class DialogueManager:
    def get_response(self, chat_history: List[Message]) -> Response:
        # Implement your dialogue logic here
        # This is a placeholder implementation
        return Response(
            intent_category=IntentCategory.ACCOUNT,
            bot_msg='Hello! How can I help you with your account?',
            is_ticket_closed=False
        )
