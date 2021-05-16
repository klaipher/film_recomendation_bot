from aiogram import types

from app.keyboards.base.start_kb import *

__all__ = ["gm_start", "gm_back"]


async def gm_start(message: types.Message) -> int:
    text = "<b>Привіт. Я - MovieBot</b>, Ваш віртуальний помічник по рекомендації кінофільмів на основі " \
           "Ваших вподобань. Чи більше буде проведено оцінювань, тим більша варіативність жанрів та " \
           "точність рекомендації кінострічок Вам буде надана. Виберіть, будь ласка, опцію з меню для початку роботи."
    message_id = (await message.answer(text, reply_markup=gen_start_kb())).message_id
    return message_id


async def gm_back(message: types.Message, text: str) -> int:
    kb = back_kb()
    message_id = (await message.answer(text, reply_markup=kb)).message_id
    return message_id
