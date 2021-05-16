from typing import Tuple, Union

from aiogram import types
from aiogram.utils.exceptions import TelegramAPIError

from app.config import movie_image


async def send_photo_by_file(
        message: types.Message, text: str, image_name: str,
        reply_markup: Union[types.InlineKeyboardMarkup, types.ReplyKeyboardMarkup, None] = None) -> Tuple[str, int]:
    with (movie_image / image_name).open("rb") as photo:
        sent_message = await message.answer_photo(
            photo, text, reply_markup=reply_markup
        )
        message_id = sent_message.message_id
        file_id = sent_message.photo[-1].file_id
    return file_id, message_id


async def gm_movie_view(
        message: types.Message, movie_info: dict,
        reply_markup: Union[types.InlineKeyboardMarkup, types.ReplyKeyboardMarkup, None] = None) -> Tuple[str, int]:
    text = f"<b>{movie_info['name']} ({movie_info['year']})</b>\n\n" \
           f"<b>Жанри:</b> <i>{movie_info['genres']}</i>\n" \
           f"<b>Режисери:</b> <i>{movie_info['directors']}</i>\n" \
           f"<b>Актори:</b> <i>{movie_info['actors']}</i>\n\n" \
           f"<b>Опис:</b> {movie_info['description']}"
    if file_id := movie_info.get("image_file_id"):
        try:
            message_id = (await message.answer_photo(
                file_id, text, reply_markup=reply_markup
            )).message_id
        except TelegramAPIError:
            file_id, message_id = await send_photo_by_file(message, text, movie_info["image_file_name"], reply_markup)
    else:
        file_id, message_id = await send_photo_by_file(message, text, movie_info["image_file_name"], reply_markup)
    return file_id, message_id
