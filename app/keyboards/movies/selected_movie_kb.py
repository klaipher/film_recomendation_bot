from typing import Optional, Tuple

from aiogram import types
from aiogram.utils.callback_data import CallbackData

from app.keyboards.movies.rate_the_movie_kb import gen_rates_kb
from app.keyboards.utils.pagination import get_pagination_buttons
from app.models.selected_movie import SelectedMovie

view_selected_movie_cb = CallbackData("view_selected_movie", "action", "page", "movie_id", "extra")


async def gen_view_selected_movie_kb(
        user_id: int, page: int) -> Tuple[Optional[int], Optional[types.InlineKeyboardMarkup]]:
    kb = types.InlineKeyboardMarkup()
    filters = {
        "user_id": user_id
    }
    pages = await SelectedMovie.count(filters=filters)
    selected_movies = await SelectedMovie.paginate(page, paginate_by=1, filters=filters)
    pg_buttons = get_pagination_buttons(pages, page, view_selected_movie_cb.new("manage", "{page}", 0, 0))

    if selected_movies:
        for rates_row in gen_rates_kb(selected_movies[0].movie_id): # noqa
            kb.row(*rates_row)
        kb.add(
            types.InlineKeyboardButton(
                "Видалити з обраних",
                callback_data=view_selected_movie_cb.new("delete", page, selected_movies[0].movie_id, 0)) # noqa
        )
        kb.row(*pg_buttons)
        return selected_movies[0].movie_id, kb # noqa
    else:
        return None, None
