from aiogram import types
from aiogram.utils.callback_data import CallbackData

__all__ = [
    "START_MENU",
    "gen_start_kb",
    "start_cb",
]


START_MENU = {
    "evaluation": "🔍 Оцінювання",
    "recommendation": "📜 Рекомендації",
    "selected_movie": "🌟 Обрані фільми",
}


start_cb = CallbackData("start", "action")


def gen_start_kb() -> types.ReplyKeyboardMarkup:
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        types.KeyboardButton(START_MENU["evaluation"]),
        [
            types.KeyboardButton(START_MENU["recommendation"]),
            types.KeyboardButton(START_MENU["selected_movie"])
        ]
    ])
    return kb
