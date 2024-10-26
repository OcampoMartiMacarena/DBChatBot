import flet as ft
from presentation.chat_view import ChatView

def main(page: ft.Page):
    chat_view = ChatView(on_send=lambda _: None, expand=True)
    page.add(chat_view)

ft.app(target=main)
