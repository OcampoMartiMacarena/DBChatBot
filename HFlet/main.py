import flet as ft
from presentation.chat_view import ChatView

def main(page: ft.Page):
    page.title = "Chat Application"
    page.add(ChatView(expand=True))

ft.app(target=main)