from typing import List

from aiogram import types

from app.keyboards.movies.recommendation_kb import gen_genres_recommendation_kb
from app.models.movie import Genre

__all__ = [
    "gm_choose_genre"
]


async def gm_choose_genre(message: types.Message, genres: List[Genre]) -> int:
    if not genres:
        text = "У вас ще немає рекомендацій, оцінюйте фільми і вони обов'язково з'являться."
    else:
        text = "Оберіть жанр в якому хочете отримати рекомендації"
    kb = gen_genres_recommendation_kb(genres)
    message_id = (await message.answer(text, reply_markup=kb)).message_id
    return message_id
