from aiogram import types

from app.keyboards.base.start_kb import *

__all__ = ["gm_start"]


async def gm_start(message: types.Message) -> int:
    text = "Привіт. <b>Я - MovieBot</b>, Ваш віртуальний помічник по рекомендації кінофільмів на основі " \
           "Ваших вподобань. Виберіть, будь ласка, опцію з меню для початку роботи."
    message_id = (await message.answer(text, reply_markup=gen_start_kb())).message_id
    return message_id
