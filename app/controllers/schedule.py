import logging
from datetime import date as date_type, timedelta
from enum import Enum

from app.models.schedule import ScheduleModel
from app.models.schedule_team import ScheduleTeamModel
from app.models.schedule_week import ScheduleWeekModel
from app.utils.api_fetcher import fetch_and_render
from app.utils.urls import UrlBuilder
from app.controllers.start import breadcrumbs
from app.menu import bot_menu

logger = logging.getLogger("nhlapi.bot")


class ScheduleCommand(Enum):
    DAY = "day"
    WEEK = "week"
    DATE = "date"
    TEAM = "team"


class ScheduleController:

    @classmethod
    async def handler(cls, chat_id: int, query: str):

        chunks = query.split("_")

        logger.info(f"User from chat id '{chat_id}' triggered callback with data: {query}")

        command = cls._parse_command(chunks)

        match command:
            case ScheduleCommand.DAY:
                return await cls._schedule_day(chat_id)
            case ScheduleCommand.WEEK:
                return await cls._schedule_week(chat_id)
            case ScheduleCommand.DATE:
                return await cls._schedule_date(chat_id, chunks)
            case ScheduleCommand.TEAM:
                return await cls._schedule_team(chat_id, chunks)
            case _:
                logger.warning(f"Unknown command received from chat '{chat_id}': {query}")
                return f"Странно, что-то всетаки пошло не так.", bot_menu.main_menu

    @staticmethod
    def _parse_command(chunks: list[str]) -> ScheduleCommand:

        if len(chunks) == 1:
            return ScheduleCommand.DAY
        try:
            return ScheduleCommand(chunks[1])
        except ValueError:
            return ScheduleCommand.DAY

    @classmethod
    async def _schedule_day(cls, chat_id: int):
        breadcrumbs[chat_id].append(f"schedule_day")
        return await fetch_and_render(
            chat_id=chat_id,
            model=ScheduleModel,
            url=UrlBuilder.build_url("schedule", date_type.today()),
            cache_key=f"schedule_date_{date_type.today().strftime("%d.%m.%Y")}"
        )

    @classmethod
    async def _schedule_week(cls, chat_id: int):
        breadcrumbs[chat_id].append(f"schedule_week")
        return await fetch_and_render(
            chat_id=chat_id,
            model=ScheduleWeekModel,
            url=UrlBuilder.build_url("schedule", date_type.today() - timedelta(days=2)),
            cache_key="schedule_week"
        )

    @classmethod
    async def _schedule_date(cls, chat_id: int, chunks: list[str]):
        breadcrumbs[chat_id].append(f"schedule_week_day")
        d, m, y = map(int, chunks[2].split("."))
        date = date_type(day=d, month=m, year=y)
        return await fetch_and_render(
            chat_id=chat_id,
            model=ScheduleModel,
            url=UrlBuilder.build_url("schedule", date),
            cache_key=f"schedule_date_{date.strftime("%d.%m.%Y")}",
            render_kwargs={"date": date}
        )

    @classmethod
    async def _schedule_team(cls, chat_id: int, chunks: list[str]):
        if len(chunks) < 3:
            breadcrumbs[chat_id].append(f"schedule_team")
            logger.info(f"User from chat id '{chat_id}' did not select a team. Showing team menu.")
            return "Выберите команду", bot_menu.schedule_team_menu

        team_abbrev = chunks[2]
        breadcrumbs[chat_id].append(f"schedule_team_{team_abbrev}")

        return await fetch_and_render(
            chat_id=chat_id,
            model=ScheduleTeamModel,
            url=UrlBuilder.build_url("schedule_team", team_abbrev),
            render_kwargs={"team_abbrev": team_abbrev},
            cache_key=f"schedule_team_{chunks[2]}"
        )

    @classmethod
    async def _breadcrumb_update(cls, key, value):
        breadcrumbs[key].append(value)
