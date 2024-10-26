from pydantic import BaseModel
from typing import List
from enum import Enum, auto

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


class Message(BaseModel):
    role: str
    content: str

class Response(BaseModel):
    intent_category: Intent
    bot_msg: str
    is_ticket_closed: bool

class DialogueManager:
    def get_response(self, chat_history: List[Message]) -> Response:
        # Implement your dialogue logic here
        # This is a placeholder implementation
        return Response(
            intent_category=Intent.ACCOUNT,
            bot_msg='Hello! How can I help you with your account?',
            is_ticket_closed=False
        )
