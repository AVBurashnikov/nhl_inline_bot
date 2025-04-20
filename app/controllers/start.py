import abc
import logging

from telegram import Update
from telegram.ext import CallbackContext

from app.menu.main import main_menu

logger = logging.getLogger("nhlapi.bot")


class StartController:

    @classmethod
    async def handler(cls, update: Update, ctx: CallbackContext):
        logger.info("Recieved '/start' command")
        await update.message.reply_text("Привет", reply_markup=main_menu)

