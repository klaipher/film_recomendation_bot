import random

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from app.core.states import base_st
from app.handlers.movies.movie import send_movie
from app.keyboards.base.start_kb import START_MENU
from app.misc import dp
from app.models.movie import Movie


@dp.message_handler(Text(equals=START_MENU["random_movie"]), chat_type=types.ChatType.PRIVATE, state=base_st.START)
async def random_movie(message: types.Message, state: FSMContext):
    count_movie = await Movie.all().count()
    await send_movie(message, random.randint(1, count_movie), state, base_st.START)
