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
            
class ChatView(ft.UserControl):
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

    def build(self):
        return ft.Column([
            self.chat_messages,
            ft.Row([
                self.user_input,
                self.send_button
            ])
        ], expand=self.expand)

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
