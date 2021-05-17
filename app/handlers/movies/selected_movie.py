from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from app.core.states import base_st, movies_st
from app.core.utils.messages import edit_message_and_delete_reply_markup, safe_delete
from app.handlers.movies.movie import send_movie
from app.keyboards.base.start_kb import START_MENU
from app.keyboards.movies.rate_the_movie_kb import rate_the_film_cb
from app.keyboards.movies.selected_movie_kb import gen_view_selected_movie_kb, view_selected_movie_cb
from app.messages_generation.base.start_gen import gm_back
from app.misc import dp
from app.models.movie_rating import MovieRating
from app.models.selected_movie import SelectedMovie


async def send_selected_movie(message: types.Message, state: FSMContext, user_id: int, page: int):
    movie_id, kb = await gen_view_selected_movie_kb(user_id, page)
    if movie_id is None:
        await message.answer("У вас ще немає обраних фільмів.")
    else:
        await send_movie(message, movie_id, state, movies_st.VIEW_SELECTED, kb)


@dp.message_handler(Text(equals=START_MENU["selected_movie"]), chat_type=types.ChatType.PRIVATE, state=base_st.START)
async def view_selected_movies(message: types.Message, state: FSMContext):
    await gm_back(message, "Обирай фільм зі своєї колекції 👇🏻")
    await send_selected_movie(message, state, message.from_user.id, 1)


@dp.callback_query_handler(view_selected_movie_cb.filter(action="manage"), chat_type=types.ChatType.PRIVATE,
                           state=movies_st.VIEW_SELECTED)
async def rate_selected_movie(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await safe_delete(call.message)
    page = int(callback_data["page"])
    await send_selected_movie(call.message, state, call.from_user.id, page)


@dp.callback_query_handler(rate_the_film_cb.filter(action="rate"), chat_type=types.ChatType.PRIVATE,
                           state=movies_st.VIEW_SELECTED)
async def rate_selected_movie(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await edit_message_and_delete_reply_markup(call.message)
    movie_id = int(callback_data["movie_id"])
    movie_score = int(callback_data["extra"])
    await (await SelectedMovie.get(id=movie_id)).delete()
    await MovieRating.create(
        user_id=call.from_user.id,
        movie_id=movie_id,
        rating=movie_score
    )
    await send_selected_movie(call.message, state, call.from_user.id, 1)


@dp.callback_query_handler(view_selected_movie_cb.filter(action="delete"), chat_type=types.ChatType.PRIVATE,
                           state=movies_st.VIEW_SELECTED)
async def rate_selected_movie(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await edit_message_and_delete_reply_markup(call.message)
    movie_id = int(callback_data["movie_id"])
    await (await SelectedMovie.get(movie_id=movie_id, user_id=call.from_user.id)).delete()
    await send_selected_movie(call.message, state, call.from_user.id, 1)
