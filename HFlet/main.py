import flet as ft
from presentation.chat_view import ChatView
from presentation.chat_model_presenter import ChatPresenter

def main(page: ft.Page):
    page.title = "Chat Application"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    chat_view = ChatView(on_send=lambda _: None, expand=True)
    chat_presenter = ChatPresenter(view=chat_view)

    def handle_send(message):
        chat_presenter.process_user_message(message)

    chat_view.on_send = handle_send

    page.add(chat_view)
    chat_presenter.start_chat()

ft.app(target=main)
