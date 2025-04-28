import abc
import logging
from collections import deque

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext

from app.controllers.game import GameSummaryController
from app.controllers.playoff import PlayoffController
from app.controllers.schedule import ScheduleController
from app.menu.bot_menu import main_menu
from app.controllers.start import breadcrumbs


logger = logging.getLogger("nhlapi.bot")


class CallbackQueryController:

    @classmethod
    async def handler(cls, upd: Update, ctx: CallbackContext):
        message = "None"
        reply_markup = None
        chat_id = upd.callback_query.message.chat.id
        query = upd.callback_query.data

        logger.info(f"Callback query '{query}' from chat id '{chat_id}' recived")

        if query == "back" and len(breadcrumbs) > 0:
            breadcrumbs[chat_id].pop()
            query = breadcrumbs[chat_id].pop()

        if query == "home":
            message, reply_markup = "Home", main_menu
            breadcrumbs[chat_id].clear()
            breadcrumbs[chat_id].append("home")

        elif query.startswith("schedule"):
            message, reply_markup = await ScheduleController.handler(chat_id, query)

        elif query.startswith("playoff"):
            message, reply_markup = await PlayoffController.handler(chat_id, query)

        elif query.startswith("game"):
            message, reply_markup = await GameSummaryController.handler(chat_id, query)

        logger.info(f"Breadcrumbs: {" -> ".join(breadcrumbs[chat_id])}")
        await upd.callback_query.edit_message_text(
            message,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )





