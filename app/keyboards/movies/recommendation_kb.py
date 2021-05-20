from typing import Optional, Tuple, List

from aiogram import types
from aiogram.utils.callback_data import CallbackData
from tortoise.query_utils import Q

from app.keyboards.utils.pagination import get_pagination_buttons
from app.models.movie import Genre, Movie

__all__ = [
    "choose_genre_cb",
    "view_recommended_movie_cb",
    "gen_genres_recommendation_kb",
    "gen_view_recommended_movie_kb",
]

from app.models.movie_rating import MovieRating
from app.models.selected_movie import SelectedMovie

choose_genre_cb = CallbackData("choose_genre", "action", "genre_id")
view_recommended_movie_cb = CallbackData("view_recommended_movie", "action", "page", "movie_id", "extra")


def calc_offset(page: int, paginate_by: int) -> int:
    if page > 0:
        page -= 1
    return page * paginate_by


def gen_genres_recommendation_kb(genres: List[Genre]) -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup()
    for genre in genres:
        kb.add(types.InlineKeyboardButton(genre.name, callback_data=choose_genre_cb.new("choose", genre.id)))
    return kb


async def gen_view_recommended_movie_kb(
        user_id: int, genre_id: int, page: int) -> Tuple[Optional[int], Optional[types.InlineKeyboardMarkup]]:
    kb = types.InlineKeyboardMarkup()
    excluded_movie_id = (rated_movie.movie_id for rated_movie in
                         [*await MovieRating.filter(user_id=user_id, didnt_see=False).all(),
                          *await SelectedMovie.filter(user_id=user_id).all()])
    actors_id = set()
    directors_id = set()
    async for movie in MovieRating.filter(
            user_id=user_id,
            rating__gte=7
    ).all().prefetch_related("movie"):
        actors_id.update(actor.id for actor in await movie.movie.actors.limit(3))
        directors_id.update(director.id for director in await movie.movie.directors.limit(1))
    selected_movies = await Movie.filter(
            Q(id__not_in=excluded_movie_id),
            Q(genres=genre_id),
            Q(actors__in=actors_id) | Q(directors__in=directors_id)
    ).distinct().all()

    if selected_movies:
        pages = len(selected_movies)
        selected_movie = selected_movies[page - 1]
        kb.add(
            types.InlineKeyboardButton(
                "Додати в обрані",
                callback_data=view_recommended_movie_cb.new("add_to_selected", page, selected_movie.id, 0))
        )
        pg_buttons = get_pagination_buttons(pages, page,
                                            view_recommended_movie_cb.new("manage", "{page}", 0, 0))
        kb.row(*pg_buttons)
        return selected_movie.id, kb
    else:
        return None, None
