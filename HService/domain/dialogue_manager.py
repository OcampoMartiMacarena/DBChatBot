from pydantic import BaseModel, Field
from typing import List
from enum import Enum, auto
import os
from dotenv import load_dotenv
import google.generativeai as genai
import instructor

class Intent(Enum):
    create_account = auto()
    delete_account = auto()
    edit_account = auto()
    recover_password = auto()
    registration_problems = auto()
    switch_account = auto()
    check_cancellation_fee = auto()
    contact_customer_service = auto()
    contact_human_agent = auto()
    delivery_options = auto()
    delivery_period = auto()
    complaint = auto()
    review = auto()
    check_invoice = auto()
    get_invoice = auto()
    cancel_order = auto()
    change_order = auto()
    place_order = auto()
    track_order = auto()
    check_payment_methods = auto()
    payment_issue = auto()
    check_refund_policy = auto()
    get_refund = auto()
    track_refund = auto()
    change_shipping_address = auto()
    set_up_shipping_address = auto()
    newsletter_subscription = auto()

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
