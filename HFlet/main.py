import flet as ft
from presentation.chat_view import ChatView
from presentation.chat_model_presenter import ChatPresenter

def main(page: ft.Page):
    page.title = "Chat Application"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    chat_view = ChatView(on_send=lambda _: None, expand=True)
    chat_presenter = ChatPresenter(view=chat_view, page=page)

    chat_presenter.set_on_send_handler(chat_view)

    end_button = ft.ElevatedButton("End Conversation", on_click=chat_presenter.end_conversation)

    page.add(chat_view, end_button)
    chat_presenter.start_chat()

ft.app(target=main)
