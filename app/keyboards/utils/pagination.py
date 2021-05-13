from aiogram import types
from telegram_bot_pagination import InlineKeyboardPaginator


def get_pagination_buttons(
    page_count: int, current_page: int, data_pattern: str, cls=InlineKeyboardPaginator
):
    paginator = cls(page_count, current_page=current_page, data_pattern=data_pattern)
    pagination_buttons = [
        types.InlineKeyboardButton(text=button["text"], callback_data=button["callback_data"])
        for button in paginator.keyboard
    ]

    return pagination_buttons
