from enum import Enum
from pydantic import BaseModel

# -------- Enum de intents --------
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

# -------- Modelos de datos --------
class Message(BaseModel):
    role: str
    content: str

class Response(BaseModel):
    thought_process_for_intent: str
    intent: Intent
    bot_msg: str
    is_ticket_closed: bool

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    in_stock: bool
    discount_percent: float