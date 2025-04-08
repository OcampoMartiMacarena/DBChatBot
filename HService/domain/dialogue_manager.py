from pydantic import BaseModel, Field
from typing import List
from enum import Enum, auto
import os
from dotenv import load_dotenv
import google.generativeai as genai
import instructor
import time
from fastapi import HTTPException

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
        
        api_key = os.environ.get("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("MISTRAL_API_KEY not found in environment variables")
        
        # Select the model and create the client
        self.model = Mistral(api_key=api_key)
        self.client = instructor.from_mistral(
            client=self.model,
            model="open-mistral-nemo",  # Verify this is the correct model
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
        IMPORTANT: Do not respond with 'Hello, how can I assist you today?' unless the chat history is empty.
        """

        self.last_request_time = 0
        self.request_interval = 1  # Minimum time between requests in seconds

    def get_response(self, chat_history: List[Message]) -> Response:
        formatted_history = self._format_chat_history(chat_history)
        print(f"Formatted chat history: {formatted_history}")  # Debug print
        
        # Implement rate limiting
        current_time = time.time()
        if current_time - self.last_request_time < self.request_interval:
            time.sleep(self.request_interval - (current_time - self.last_request_time))
        self.last_request_time = time.time()

        prompt = f"""
        Given the following chat history, provide an appropriate response:

        Chat History:
        {formatted_history}

        Respond with the intent category, bot message, and whether the ticket should be closed.
        Remember to analyze the chat history and provide a contextual response.
        Do not repeat previous bot messages. Provide new, relevant information or ask for more details.
        """

        messages = [
            {"role": "system", "content": self.system_message},
            {"role": "user", "content": prompt}
        ]

        try:
            response = self.client.chat.completions.create(
                messages=messages,
                response_model=Response
            )
            print(f"Raw response from Mistral: {response}")  # Debug print
            return response
        except Exception as e:
            print(f"Error occurred while getting response from Mistral: {str(e)}")
            if "rate limit exceeded" in str(e).lower():
                raise HTTPException(status_code=429, detail="Too many requests. Please try again later.")
            raise HTTPException(status_code=500, detail="An error occurred while processing your request.")

    def _format_chat_history(self, chat_history: List[Message]) -> str:
        if not chat_history:
            return "No previous messages."
        return "\n".join([f"{msg.role}: {msg.content}" for msg in chat_history])
