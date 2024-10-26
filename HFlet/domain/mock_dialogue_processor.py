from typing import List, Tuple
import random

class Message:
    def __init__(self, sender: str, msg: str):
        self.sender = sender
        self.msg = msg

class ChatHistoryManager:
    def __init__(self):
        self.chat_history: List[Message] = []
        self.bot_msg: str = ""
        self.is_ticket_closed: bool = False

    def add_message(self, sender: str, msg: str):
        self.chat_history.append(Message(sender, msg))

    def set_bot_response(self, response: str, ticket_closed: bool):
        self.bot_msg = response
        self.is_ticket_closed = ticket_closed

    def save_last_message(self):
        if self.bot_msg:
            self.add_message("bot", self.bot_msg)
            self.bot_msg = ""

class MockDialogueProcessor:
    def __init__(self):
        self.responses = {
            "hello": [
                "Hello! Welcome to our customer support. How may I assist you today?",
                "Hi there! Thank you for contacting our support team. What can I help you with?",
                "Greetings! I'm here to help with any questions or issues you might have. What brings you to our support today?"
            ],
            "issue": [
                "I'm sorry to hear you're experiencing an issue. Could you please provide more details about what's happening?",
                "I understand you're facing a problem. Can you describe the issue in more detail so I can better assist you?",
                "Thank you for reporting this. To help you effectively, could you explain the issue you're encountering?"
            ],
            "product": [
                "Certainly! I'd be happy to provide information about our products. Which specific product are you interested in?",
                "Of course, I can help with product information. Could you tell me which product you'd like to know more about?",
                "I'd be glad to assist with product details. Which particular product are you inquiring about?"
            ],
            "help": [
                "I'm here to help! Could you please specify what kind of assistance you need?",
                "Absolutely, I'm here to assist. What particular area do you need help with?",
                "I'd be happy to help you. Can you provide more information about what you need assistance with?"
            ],
        }

    def generate_response(self, chat_manager: ChatHistoryManager) -> None:
        if not chat_manager.chat_history:
            response = random.choice(self.responses["hello"])
            chat_manager.set_bot_response(response, False)
            return

        last_message = chat_manager.chat_history[-1].msg.lower().strip()
        
        for key, responses in self.responses.items():
            if key in last_message:
                response = random.choice(responses)
                chat_manager.set_bot_response(response, False)
                return

        # Check if the conversation should be closed
        if "goodbye" in last_message or "thank you" in last_message:
            response = "Thank you for contacting our support team. Is there anything else I can help you with before we conclude our chat?"
            chat_manager.set_bot_response(response, True)
            return

        response = "I apologize, but I'm not sure I fully understood your question. Could you please provide more details or rephrase your inquiry? I'm here to help and want to make sure I address your needs correctly."
        chat_manager.set_bot_response(response, False)
