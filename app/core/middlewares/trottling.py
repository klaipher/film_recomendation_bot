from aiogram import Dispatcher, types
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled

from app.core.utils.messages import delete_message_by_id_after


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit=1, key_prefix="antiflood_"):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def check_throttling(self, message: types.Message, _: dict):
        handler = current_handler.get()

        dispatcher = Dispatcher.get_current()
        # If handler was configured, get rate limit and key from handler
        if handler:
            limit = getattr(handler, "throttling_rate_limit", self.rate_limit)
            key = getattr(handler, "throttling_key", f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"

        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            await self.message_throttled(message, t)
            raise CancelHandler()

    @staticmethod
    async def message_throttled(message: types.Message, throttled: Throttled):

        if throttled.exceeded_count <= 2:
            sent_message = await message.answer("Занадто багато запитів!")
            delete_message_by_id_after(10, sent_message.chat.id, sent_message.message_id)

    async def on_pre_process_callback_query(self, call: types.CallbackQuery, data: dict):
        self.rate_limit = 0.4
        await self.check_throttling(call.message, data)

    async def on_pre_process_message(self, message: types.Message, data: dict):
        self.rate_limit = 0.8
        await self.check_throttling(message, data)
