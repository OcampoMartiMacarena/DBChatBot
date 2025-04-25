import flet as ft
from typing import Callable

class InputRow(ft.Row):
    def __init__(self, on_submit, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_input = ft.Ref[ft.TextField]()
        self.submit_button = ft.Ref[ft.ElevatedButton]()
        self.on_submit = on_submit

    def build(self):
        self.controls = [
            ft.TextField(
                ref=self.text_input,
                label="Enter text",
                on_submit=self.on_submit,
                expand=True
            ),
            ft.ElevatedButton(
                ref=self.submit_button,
                text="Submit",
                on_click=self.on_submit
            )
        ]

class MessageBubble(ft.Container):
    def __init__(self, message: str, is_user: bool):
        super().__init__()
        self.padding = ft.padding.all(8)
        self.border_radius = ft.border_radius.all(10)
        self.bgcolor = "#F0636C" if is_user else "#4A5459"  # Coral-red for user, dark blue-gray for bot
        
        text = ft.Text(
            message,
            size=14,
            overflow=ft.TextOverflow.VISIBLE,
            no_wrap=False,
            text_align=ft.TextAlign.LEFT,
            color="white",  # White text for both user and bot messages
        )
        
        text_container = ft.Container(
            content=text,
            padding=ft.padding.all(4),
            alignment=ft.alignment.center_left,
        )
        
        self.content = text_container
        self.alignment = ft.alignment.center_right if is_user else ft.alignment.center_left
        
        # Adjust margins for message alignment
        if is_user:
            self.margin = ft.margin.only(left=80, right=10, top=5, bottom=5)
        else:
            self.margin = ft.margin.only(left=10, right=80, top=5, bottom=5)
            
class ChatView(ft.Container):  # Changed from ft.View to ft.Container
    def __init__(self, on_send: Callable[[str], None], expand: bool = False):
        super().__init__()
        self.on_send = on_send
        self.expand = expand
        self.chat_messages = ft.Column(scroll="auto", expand=True)
        self.user_input = ft.TextField(
            hint_text="Type your message here...",
            expand=True,
            on_submit=self.send_message
        )
        self.send_button = ft.IconButton(
            icon=ft.icons.SEND,
            on_click=self.send_message
        )
        self.end_conversation_button = ft.ElevatedButton(
            text="End Conversation",
            on_click=self.show_ticket_closed_popup
        )
        self.new_ticket_button = ft.ElevatedButton(
            text="Open New Ticket",
            on_click=self.start_new_conversation,
            visible=False
        )
        
        # Set the content directly in the constructor
        self.content = ft.Column([
            self.chat_messages,
            ft.Row([
                self.user_input,
                self.send_button
            ]),
            self.end_conversation_button,
        ], expand=self.expand)
        
        # Set container properties
        self.expand = expand
        self.padding = ft.padding.all(10)

    def send_message(self, _):
        message = self.user_input.value
        if message:
            self.on_send(message)

    def get_user_message(self) -> str:
        return self.user_input.value

    def display_bot_message(self, message: str):
        self.chat_messages.controls.append(MessageBubble(message, is_user=False))
        self.chat_messages.update()

    def display_user_message(self, message: str):
        self.chat_messages.controls.append(MessageBubble(message, is_user=True))
        self.chat_messages.update()

    def clear_user_input(self):
        self.user_input.value = ""
        self.user_input.update()

    def show_loading_indicator(self):
        self.chat_messages.controls.append(ft.ProgressRing())
        self.chat_messages.update()

    def hide_loading_indicator(self):
        if isinstance(self.chat_messages.controls[-1], ft.ProgressRing):
            self.chat_messages.controls.pop()
            self.chat_messages.update()

    def show_ticket_closed_popup(self, _):
        def close_dlg(_):
            self.page.dialog.open = False
            self.page.update()
            self.end_conversation()

        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Ticket Closed"),
            content=ft.Text("The conversation has ended and the ticket is now closed."),
            actions=[
                ft.TextButton("OK", on_click=close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog.open = True
        self.page.update()

    def end_conversation(self):
        # Display chat history in console
        self.display_chat_history()
        
        # Clear all messages
        self.chat_messages.controls.clear()
        
        # Hide input row and end conversation button
        self.user_input.visible = False
        self.send_button.visible = False
        self.end_conversation_button.visible = False
        
        # Show "Open New Ticket" button in the middle
        self.new_ticket_button.visible = True
        
        # Center the "Open New Ticket" button
        self.chat_messages.controls.append(
            ft.Container(
                content=self.new_ticket_button,
                alignment=ft.alignment.center,
                expand=True
            )
        )
        
        self.update()

    def start_new_conversation(self, _):
        # Clear the chat messages
        self.chat_messages.controls.clear()
        
        # Show input row and end conversation button
        self.user_input.visible = True
        self.send_button.visible = True
        self.end_conversation_button.visible = True
        
        # Hide "Open New Ticket" button
        self.new_ticket_button.visible = False
        
        self.update()

    def display_chat_history(self):
        print("Chat History:")
        for message in self.chat_messages.controls:
            if isinstance(message, MessageBubble):
                sender = "User" if message.alignment == ft.alignment.center_right else "Bot"
                print(f"{sender}: {message.content.content.value}")
        print("End of Chat History")
