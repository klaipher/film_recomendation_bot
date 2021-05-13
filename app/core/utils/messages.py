import asyncio
import datetime
from contextlib import suppress

from aiogram import Bot, types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import (
    MessageCantBeDeleted,
    MessageToDeleteNotFound,
    TelegramAPIError,
)
from apscheduler.job import Job

from app.models.user import User
from app.services.apscheduller import scheduler

__all__ = [
    "safe_delete",
    "delete_message",
    "delete_message_by_id",
    "delete_error_message",
    "delete_message_by_id_after",
    "delete_all",
    "clear_reply_kb",
    "delete_message_by_data_id",
    "create_fake_message",
    "start_mailing",
]


async def safe_delete(message: types.Message):
    with suppress(MessageToDeleteNotFound, MessageCantBeDeleted):
        await message.delete()


async def delete_message_by_id(chat_id: int, message_id: int):
    bot = Bot.get_current()
    with suppress(TelegramAPIError):
        await bot.delete_message(chat_id, message_id)


async def delete_message_by_data_id(key: str, state: FSMContext):
    async with state.proxy() as data:
        if data.get(key):
            await delete_message_by_id(state.chat, data[key])


async def delete_message(state: FSMContext):
    await delete_message_by_data_id("message_id", state)


async def delete_error_message(state: FSMContext):
    await delete_message_by_data_id("error_message_id", state)


def delete_message_by_id_after(time: int, chat_id: int, message_id: int) -> Job:
    job = scheduler.add_job(
        delete_message_by_id,
        "date",
        id=f"TIMER:DELETE:AFTER_{time}:{chat_id}{message_id}",
        run_date=datetime.datetime.utcnow() + datetime.timedelta(seconds=time),
        kwargs={"chat_id": chat_id, "message_id": message_id},
    )
    return job


async def delete_all(state: FSMContext):
    await delete_error_message(state)
    await delete_message(state)


async def clear_reply_kb(message: types.Message, after: int = 1, text: str = "🗝🗝🗝"):
    sent_msg = await message.answer(text, reply_markup=types.ReplyKeyboardRemove())
    delete_message_by_id_after(after, sent_msg.chat.id, sent_msg.message_id)


def create_fake_message(user_id: int) -> types.Message:
    return types.Message(from_user=types.User(id=user_id), chat=types.Chat(id=user_id))


async def start_mailing(message: types.Message):
    users = await User.all()
    for user in users:
        with suppress(TelegramAPIError):
            await message.send_copy(user.id)
            await asyncio.sleep(0.3)
