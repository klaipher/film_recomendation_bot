from aiogram import md, types
from aiogram.dispatcher.middlewares import BaseMiddleware

from app.models.user import User


class ACLMiddleware(BaseMiddleware):
    @staticmethod
    async def setup_chat(data: dict, user: types.User):

        user_db: User = await User.filter(id=user.id).first()

        if user_db is None:
            user_db = await User.create(
                id=user.id, name=md.quote_html(user.full_name), username=user.username, lang="uk"
            )
        else:
            user_db.username = user.username
            user_db.name = md.quote_html(user.full_name)
            await user_db.save()

        data["user"] = user_db

    async def on_pre_process_message(self, message: types.Message, data: dict):
        await self.setup_chat(data, message.from_user)

    async def on_pre_process_callback_query(self, call: types.CallbackQuery, data: dict):
        await self.setup_chat(data, call.from_user)
