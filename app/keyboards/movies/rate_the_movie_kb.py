from typing import Tuple, List

from aiogram import types
from aiogram.utils.callback_data import CallbackData

__all__ = [
    "rate_the_film_cb",
    "rate_movie_kb",
    "gen_rates_kb",
]

rate_the_film_cb = CallbackData("rate_movie", "action", "movie_id", "extra")


def gen_rates_kb(movie_id: int) -> Tuple[List[types.InlineKeyboardButton], List[types.InlineKeyboardButton]]:
    return ([
                types.InlineKeyboardButton(rating, callback_data=rate_the_film_cb.new("rate", movie_id, index))
                for index, rating in enumerate(["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"], start=1)
            ],
            [
                types.InlineKeyboardButton(rating, callback_data=rate_the_film_cb.new("rate", movie_id, index))
                for index, rating in enumerate(["6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"], start=6)
            ])


def rate_movie_kb(movie_id: int) -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup()
    for rates_row in gen_rates_kb(movie_id):
        kb.row(*rates_row)
    kb.add(types.InlineKeyboardButton("Не бачив", callback_data=rate_the_film_cb.new("didnt_see", movie_id, 0)))
    kb.add(types.InlineKeyboardButton("Додати в обрані",
                                      callback_data=rate_the_film_cb.new("add_to_selected", movie_id, 0)))
    return kb
