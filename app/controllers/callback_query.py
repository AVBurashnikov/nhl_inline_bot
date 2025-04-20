import abc

from telegram import Update
from telegram.ext import CallbackContext

from app.controllers.schedule import ScheduleController
from app.menu.main import main_menu


class CallbackQueryController:

    @classmethod
    async def handler(cls, update: Update, ctx: CallbackContext):
        query = update.callback_query
        message = "None"
        reply_markup = None
        if query.data == "schedule":
            message, reply_markup = await ScheduleController.handler(update, ctx)

        elif query.data == "main_menu":
            message, reply_markup = "MainMenu", main_menu

        await query.edit_message_text(message, reply_markup=reply_markup)





