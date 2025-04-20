from telegram import Update
from telegram.ext import CallbackContext

from app.menu.schedule import schedule_menu


class ScheduleController:

    @classmethod
    async def handler(cls, update: Update, ctx: CallbackContext):
        return "Shedule", schedule_menu
