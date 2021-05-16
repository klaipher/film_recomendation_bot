from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from app.core.states import base_st, movies_st
from app.core.utils.messages import safe_delete, edit_message_and_delete_reply_markup
from app.handlers.movies.movie import send_movie
from app.keyboards.base.start_kb import START_MENU
from app.keyboards.movies.recommendation_kb import choose_genre_cb, gen_view_recommended_movie_kb, \
    view_recommended_movie_cb
from app.messages_generation.base.start_gen import gm_back
from app.messages_generation.movies.recommendation_gen import gm_choose_genre
from app.misc import dp
from app.models.movie_rating import MovieRating
from app.models.selected_movie import SelectedMovie


async def send_recommended_movie(message: types.Message, state: FSMContext, user_id: int, genre_id: int, page: int):
    movie_id, kb = await gen_view_recommended_movie_kb(user_id, genre_id, page)
    if movie_id is None:
        await message.answer("В цій категорії для вас немає рекомендацій.")
    else:
        await send_movie(message, movie_id, state, movies_st.MOVIE_RECOMMENDATION, kb)


@dp.message_handler(Text(equals=START_MENU["recommendation"]), chat_type=types.ChatType.PRIVATE, state=base_st.START)
async def recommendation(message: types.Message, state: FSMContext):
    good_rated_movies = await MovieRating.filter(
        user_id=message.from_user.id,
        rating__gte=7
    ).all().prefetch_related("movie")
    genres = []
    for movie in good_rated_movies:
        genres.extend(filter(lambda i: i not in genres, await movie.movie.genres.all()))
    async with state.proxy() as data:
        data["message_id"] = await gm_choose_genre(message, genres)
    if genres:
        await state.set_state(movies_st.MOVIE_RECOMMENDATION)


@dp.callback_query_handler(choose_genre_cb.filter(action="choose"), chat_type=types.ChatType.PRIVATE,
                           state=movies_st.MOVIE_RECOMMENDATION)
@dp.callback_query_handler(view_recommended_movie_cb.filter(action="manage"), chat_type=types.ChatType.PRIVATE,
                           state=movies_st.MOVIE_RECOMMENDATION)
async def recommendation_based_on_genre(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await safe_delete(call.message)
    page = int(callback_data.get("page", 1))
    async with state.proxy() as data:
        data["current_page"] = page
        if (genre_id := int(callback_data.get("genre_id", 0))) != 0:
            data["current_genre_id"] = genre_id
            await gm_back(call.message, "Обирай жанр рекомендацій 👇🏻")
        else:
            genre_id = data["current_genre_id"]
    await send_recommended_movie(call.message, state, call.from_user.id, genre_id, page)


@dp.callback_query_handler(view_recommended_movie_cb.filter(action="add_to_selected"), chat_type=types.ChatType.PRIVATE,
                           state=movies_st.MOVIE_RECOMMENDATION)
async def add_to_selected(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await edit_message_and_delete_reply_markup(call.message)
    movie_id = int(callback_data["movie_id"])
    await SelectedMovie.create(
        user_id=call.from_user.id,
        movie_id=movie_id,
    )
    async with state.proxy() as data:
        if data["current_page"] <= 1:
            page = 1
        else:
            page = data["current_page"] - 1
        genre_id = data["current_genre_id"]
    await send_recommended_movie(call.message, state, call.from_user.id, genre_id, page)
