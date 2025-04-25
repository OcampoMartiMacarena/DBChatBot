import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="google._upb._message")

import os
import json
import re
import time
from typing import List
from dotenv import load_dotenv
import google.generativeai as genai
from fastapi import HTTPException
from pydantic import ValidationError

from HService.domain.models import Intent, Message, Response, Product
from HService.service.product_service import get_all_products


# ---------------- Gemini Wrapper ----------------
class GeminiWrapper:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-pro")
        self.last_request_time = 0
        self.request_interval = 0

    def extract_first_json_block(self, text: str) -> str:
        match = re.search(r'{.*}', text, re.DOTALL)
        if match:
            return match.group(0)
        else:
            raise ValueError("No valid JSON block found.")

    def send(self, prompt: str, response_model):
        try:
            response = self.model.generate_content(prompt)
            content = response.text.strip()
            print("Raw Gemini response:\n", content)  # Debug print

            try:
                json_str = self.extract_first_json_block(content)
                data = json.loads(json_str)

                if "intent" in data and data["intent"] not in [e.value for e in Intent]:
                    raise HTTPException(status_code=500, detail=f"Invalid intent value: {data['intent']}")

                return response_model(**data)
            except (json.JSONDecodeError, ValidationError, ValueError) as e:
                print(f"Error parsing response: {e}")
                raise HTTPException(status_code=500, detail="Invalid response format from Gemini.")

        except Exception as e:
            print(f"Error while contacting Gemini: {str(e)}")
            if "rate limit" in str(e).lower():
                raise HTTPException(status_code=429, detail="Too many requests. Please try again later.")
            raise HTTPException(status_code=500, detail="An error occurred while processing your request.")

# ---------------- Dialogue Manager ----------------
class DialogueManager:
    def __init__(self):
        self.gemini = GeminiWrapper()
        self.system_message = (
            "You are an expert AI customer service assistant trained to resolve all user requests without human intervention. "
            "You are autonomous and confident in your answers, and never refer the user to a human agent. "
            "Always analyze the chat history carefully, detect the user's intent, and respond with helpful, complete, and proactive solutions. "
            "IMPORTANT: Never say that you are an AI or mention that you cannot do something. "
            "Do not ask if the user wants to be transferred or say that an agent will join. "
            "Your job is to fully handle the situation until the ticket can be closed."
        )

    def get_response(self, chat_history: List[Message]) -> Response:
        formatted_history = self._format_chat_history(chat_history)

        # Traer productos desde base de datos
        products = get_all_products()
        product_info = "\n".join([
            f"- {p.name}: {p.description}. Precio: ${p.price}. Stock: {'Sí' if p.in_stock else 'No'}. Descuento: {p.discount_percent}%."
            for p in products
        ])

        valid_intents = ', '.join([f'"{e.value}"' for e in Intent])

        prompt = f"""
{self.system_message}

Estos son los productos disponibles actualmente:

{product_info}

Historial del chat:
{formatted_history}

Respondé solo con un objeto JSON como este:
{{
  "thought_process_for_intent": "...",
  "intent": uno de los siguientes valores: {valid_intents},
  "bot_msg": "...",
  "is_ticket_closed": true
}}

Usá los datos reales de productos cuando sea relevante.
Nunca inventes productos. No uses otros valores de intención que no estén listados.
Respondé de forma clara, breve, y útil, como un agente experto.
"""
        return self.gemini.send(prompt, response_model=Response)

    def _format_chat_history(self, chat_history: List[Message]) -> str:
        if not chat_history:
            return "No previous messages."
        return "\n".join([f"{msg.role}: {msg.content}" for msg in chat_history])