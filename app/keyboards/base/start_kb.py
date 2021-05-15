from aiogram import types
from aiogram.utils.callback_data import CallbackData

__all__ = [
    "START_MENU",
    "gen_start_kb",
    "start_cb",
    "back_kb",
    "BACK_KB",
]


START_MENU = {
    "random_movie": "🎲 Випадкова рекомендація",
    "evaluation": "🔍 Оцінювання",
    "recommendation": "📜 Рекомендації",
    "selected_movie": "🌟 Обрані фільми",
}
BACK_KB = "⬅️ Назад"

start_cb = CallbackData("start", "action")


def back_kb() -> types.ReplyKeyboardMarkup:
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton(BACK_KB))
    return kb


def gen_start_kb() -> types.ReplyKeyboardMarkup:
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [types.KeyboardButton(START_MENU["random_movie"])],
        [types.KeyboardButton(START_MENU["evaluation"])],
        [
            types.KeyboardButton(START_MENU["recommendation"]),
            types.KeyboardButton(START_MENU["selected_movie"])
        ]
    ])
    return kb
