from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from app.core.states import base_st, movies_st
from app.core.utils.messages import edit_message_and_delete_reply_markup
from app.handlers.movies.movie import send_movie
from app.keyboards.base.start_kb import START_MENU
from app.keyboards.movies.rate_the_movie_kb import rate_the_film_cb, rate_movie_kb
from app.messages_generation.base.start_gen import gm_back
from app.misc import dp
from app.models.movie import Movie
from app.models.movie_rating import MovieRating
from app.models.selected_movie import SelectedMovie


async def send_movie_for_evaluation(message: types.Message, user_id: int, state: FSMContext):
    excluded_movie_id = (rated_movie.movie_id for rated_movie in [*await MovieRating.filter(user_id=user_id).all(),
                                                                  *await SelectedMovie.filter(user_id=user_id).all()])
    movie: Movie = await Movie.filter(
        id__not_in=excluded_movie_id).first().prefetch_related("image", "directors", "genres", "actors")
    if not movie:
        await message.answer("Немає фільмів для оцінювання.")
    await send_movie(message, movie.id, state, movies_st.RATE_MOVIE, rate_movie_kb(movie.id))


@dp.message_handler(Text(equals=START_MENU["evaluation"]), chat_type=types.ChatType.PRIVATE, state=base_st.START)
async def evaluate_movie(message: types.Message, state: FSMContext):
    await gm_back(message, "Починай оцінювати фільми 👇🏻")
    await send_movie_for_evaluation(message, message.from_user.id, state)


@dp.callback_query_handler(rate_the_film_cb.filter(action="rate"), chat_type=types.ChatType.PRIVATE,
                           state=movies_st.RATE_MOVIE)
async def rate_movie(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await edit_message_and_delete_reply_markup(call.message)
    movie_id = int(callback_data["movie_id"])
    movie_score = int(callback_data["extra"])
    await MovieRating.create(
        user_id=call.from_user.id,
        movie_id=movie_id,
        rating=movie_score
    )
    await send_movie_for_evaluation(call.message, call.from_user.id, state)


@dp.callback_query_handler(rate_the_film_cb.filter(action="didnt_see"), chat_type=types.ChatType.PRIVATE,
                           state=movies_st.RATE_MOVIE)
async def didnt_see(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await edit_message_and_delete_reply_markup(call.message)
    movie_id = int(callback_data["movie_id"])
    await MovieRating.create(
        user_id=call.from_user.id,
        movie_id=movie_id,
        didnt_see=True
    )
    await send_movie_for_evaluation(call.message, call.from_user.id, state)


@dp.callback_query_handler(rate_the_film_cb.filter(action="add_to_selected"), chat_type=types.ChatType.PRIVATE,
                           state=movies_st.RATE_MOVIE)
async def add_to_selected(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await edit_message_and_delete_reply_markup(call.message)
    movie_id = int(callback_data["movie_id"])
    await SelectedMovie.create(
        user_id=call.from_user.id,
        movie_id=movie_id,
    )
    await send_movie_for_evaluation(call.message, call.from_user.id, state)
