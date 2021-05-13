from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from app.core.states import base_st
from app.core.utils.messages import safe_delete
from app.keyboards.base.start_kb import start_cb
from app.messages_generation.base.start_gen import *
from app.misc import dp


async def send_start_layout(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["message_id"] = await gm_start(message)
        await state.set_state(base_st.START)


@dp.message_handler(CommandStart(), chat_type=types.ChatType.PRIVATE, state="*")
async def cmd_start(message: types.Message, state: FSMContext):
    await send_start_layout(message, state)


@dp.callback_query_handler(start_cb.filter(action="back_to_menu"), state="*")
async def back_to_main_menu(call: types.CallbackQuery, state: FSMContext):
    await safe_delete(call.message)
    await send_start_layout(call.message, state)
