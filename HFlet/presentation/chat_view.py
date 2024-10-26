import flet as ft
from .chat_model_presenter import ChatPresenter

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
        self.bgcolor = "#EC6C5B" if is_user else "#FFA07A"  # Different colors for user and bot messages
        
        text = ft.Text(
            message,
            size=14,
            overflow=ft.TextOverflow.VISIBLE,  # Allow the text to be fully visible
            no_wrap=False,  # Enable wrapping for long messages
            text_align=ft.TextAlign.LEFT,  # Ensure text aligns from left to right
        )
        
        text_container = ft.Container(
            content=text,
            padding=ft.padding.all(4),
            alignment=ft.alignment.center_left,  # Align text to the left within the container
        )
        
        self.content = text_container
        self.alignment = ft.alignment.center_right if is_user else ft.alignment.center_left
        
        # Adjust margins for message alignment
        if is_user:
            self.margin = ft.margin.only(left=80, right=10, top=5, bottom=5)
        else:
            self.margin = ft.margin.only(left=10, right=80, top=5, bottom=5)
            
class ChatView(ft.Container):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.presenter = ChatPresenter(self)
        self.input_row = ft.Ref[InputRow]()
        self.messages_column = ft.Column(scroll="auto", expand=True, spacing=10)

    def build(self):
        self.content = ft.Column([
            ft.Text("Chat", size=20, weight="bold"),
            self.messages_column,
            InputRow(
                ref=self.input_row,
                on_submit=self.on_submit,
            )
        ], expand=True)

    def on_submit(self, e):
        text = self.input_row.current.text_input.current.value
        if text.strip():
            self.add_message(text, is_user=True)
            self.presenter.process_user_message(text)
            self.clear_input()

    def add_message(self, message: str, is_user: bool):
        self.messages_column.controls.append(MessageBubble(message, is_user))
        self.update()

    def clear_input(self):
        self.input_row.current.text_input.current.value = ""
        self.update()

    # Implement ViewProtocol methods
    def get_user_message(self) -> str:
        return self.input_row.current.text_input.current.value

    def display_bot_message(self, message: str):
        self.add_message(message, is_user=False)

    def clear_user_input(self):
        self.clear_input()

    def show_loading_indicator(self):
        # Implement loading indicator if needed
        pass

    def hide_loading_indicator(self):
        # Implement hiding loading indicator if needed
        pass
