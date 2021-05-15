from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text

from app.core.states import base_st
from app.core.utils.messages import delete_message
from app.keyboards.base.start_kb import BACK_KB
from app.messages_generation.base.start_gen import *
from app.misc import dp


async def send_start_layout(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["message_id"] = await gm_start(message)
        await state.set_state(base_st.START)


@dp.message_handler(CommandStart(), chat_type=types.ChatType.PRIVATE, state="*")
async def cmd_start(message: types.Message, state: FSMContext):
    await delete_message(state)
    await send_start_layout(message, state)


@dp.message_handler(Text(equals=BACK_KB), state="*")
async def back_to_main_menu(message: types.Message, state: FSMContext):
    await delete_message(state)
    await send_start_layout(message, state)
