import typing

from aiogram import types
from aiogram.dispatcher import FSMContext

from app.messages_generation.movies import gm_movie_view
from app.models.movie import Movie


async def send_movie(
        message: types.Message,
        movie_id: int,
        state: FSMContext,
        state_to_set: typing.Optional[typing.AnyStr],
        reply_markup: typing.Union[types.InlineKeyboardMarkup, types.ReplyKeyboardMarkup, None] = None,
):
    movie: Movie = await Movie.get(id=movie_id).prefetch_related("image", "directors", "genres", "actors")
    movie_info = {
        "id": movie.id,
        "name": movie.name,
        "year": movie.year,
        "description": movie.description,
        "actors": ", ".join(actor.name for actor in movie.actors.related_objects),
        "directors": ", ".join(director.name for director in movie.directors.related_objects),
        "genres": ", ".join(genre.name for genre in movie.genres.related_objects),
        "image_file_name": movie.image.file_name,
        "image_file_id": movie.image.file_id
    }
    async with state.proxy() as data:
        file_id, data["message_id"] = await gm_movie_view(message, movie_info, reply_markup=reply_markup)
        await state.set_state(state_to_set)
    if file_id != movie.image.file_id:
        movie.image.file_id = file_id
        await movie.image.save()
