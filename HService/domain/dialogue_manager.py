from pydantic import BaseModel, Field
from typing import List
from enum import Enum, auto
import os
from dotenv import load_dotenv
import google.generativeai as genai
import instructor

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
    def __init__(self):
        # Load environment variables and configure the API key
        load_dotenv()
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

        # Select the model and create the client
        self.model = genai.GenerativeModel('gemini-1.5-pro')
        self.client = instructor.from_gemini(client=self.model, mode=instructor.Mode.GEMINI_JSON)

        self.system_message = """
        You are an AI assistant for a customer service chatbot. Analyze the chat history and provide an appropriate response.
        Determine the intent category, generate a bot message, and decide if the ticket should be closed.
        """

    def get_response(self, chat_history: List[Message]) -> Response:
        prompt = f"""
        Given the following chat history, provide an appropriate response:

        Chat History:
        {self._format_chat_history(chat_history)}

        Respond with the intent category, bot message, and whether the ticket should be closed.
        """

        messages = [
            {"role": "system", "content": self.system_message},
            {"role": "user", "content": prompt}
        ]

        response = self.client.chat.completions.create(
            messages=messages,
            response_model=Response
        )

        return response

    def _format_chat_history(self, chat_history: List[Message]) -> str:
        return "\n".join([f"{msg.role}: {msg.content}" for msg in chat_history])
