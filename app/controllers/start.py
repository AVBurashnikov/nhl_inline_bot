import logging

from telegram import Update, Message
from telegram.ext import CallbackContext

from app.menu.bot_menu import main_menu

logger = logging.getLogger("nhlapi.bot")

breadcrumbs: dict[int, list[str]] = {}


class StartController:

    single_message: Message = None

    @classmethod
    async def handler(cls, upd: Update, ctx: CallbackContext):

        chat_id = upd.message.chat_id
        logger.info(f"Recieved '/start' command from chat id '{chat_id}'")

        if cls.single_message is not None:
            await cls.single_message.delete()

        breadcrumbs[chat_id] = ["home"]

        cls.single_message = await upd.message.reply_text("Привет", reply_markup=main_menu)
        await upd.message.delete()
