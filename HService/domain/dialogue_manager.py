from pydantic import BaseModel, Field
from typing import List
from enum import Enum, auto
import os
from dotenv import load_dotenv
import google.generativeai as genai
import instructor

from mistralai import Mistral


class Intent(str, Enum):
    create_account = "create_account"
    delete_account = "delete_account"
    edit_account = "edit_account"
    recover_password = "recover_password"
    registration_problems = "registration_problems"
    switch_account = "switch_account"
    check_cancellation_fee = "check_cancellation_fee"
    contact_customer_service = "contact_customer_service"
    contact_human_agent = "contact_human_agent"
    delivery_options = "delivery_options"
    delivery_period = "delivery_period"
    complaint = "complaint"
    review = "review"
    check_invoice = "check_invoice"
    get_invoice = "get_invoice"
    cancel_order = "cancel_order"
    change_order = "change_order"
    place_order = "place_order"
    track_order = "track_order"
    check_payment_methods = "check_payment_methods"
    payment_issue = "payment_issue"
    check_refund_policy = "check_refund_policy"
    get_refund = "get_refund"
    track_refund = "track_refund"
    change_shipping_address = "change_shipping_address"
    set_up_shipping_address = "set_up_shipping_address"
    newsletter_subscription = "newsletter_subscription"

class Message(BaseModel):
    role: str
    content: str

class Response(BaseModel):
    thought_process_for_intent: str
    intent: Intent
    bot_msg: str
    is_ticket_closed: bool

class DialogueManager:
    def __init__(self):
        # Load environment variables and configure the API key
        load_dotenv()

        # Select the model and create the client
        self.model = Mistral(api_key=os.environ.get("MISTRAL_API_KEY"))
        self.client = instructor.from_mistral(
            client=self.model,
            model="open-mistral-nemo",
            mode=instructor.Mode.MISTRAL_TOOLS,
            max_tokens=1000,
        )

        # # Select the model and create the client
        # genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        # self.model = genai.GenerativeModel('gemini-1.5-flash')
        # self.client = instructor.from_gemini(client=self.model, mode=instructor.Mode.GEMINI_JSON)

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

        print(response)

        return response

    def _format_chat_history(self, chat_history: List[Message]) -> str:
        return "\n".join([f"{msg.role}: {msg.content}" for msg in chat_history])
