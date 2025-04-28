import logging
from enum import Enum

from app.controllers.start import breadcrumbs
from app.models.playoff import PlayoffModel
from app.models.playoff_series import PlayoffSeriesModel
from app.utils.api_fetcher import fetch_and_render
from app.utils.urls import UrlBuilder

logger = logging.getLogger("nhlapi.bot")


class PlayoffCommand(Enum):
    PLAYOFF = "playoff"
    PLAYOFF_SERIES = "series"


class PlayoffController:

    @classmethod
    async def handler(cls, chat_id: int, query: str):

        chunks = query.split("_")

        logger.info(f"User from chat id '{chat_id}' triggered callback with data: {query}")

        command = cls._parse_command(chunks)

        match command:
            case PlayoffCommand.PLAYOFF:
                return await cls._playoff(chat_id)
            case PlayoffCommand.PLAYOFF_SERIES:
                return await cls._playoff_series(chat_id, chunks)

    @staticmethod
    def _parse_command(chunks: list[str]) -> PlayoffCommand:

        if len(chunks) == 1:
            return PlayoffCommand.PLAYOFF
        try:
            return PlayoffCommand(chunks[1])
        except ValueError:
            return PlayoffCommand.PLAYOFF

    @classmethod
    async def _playoff(cls, chat_id: int):
        breadcrumbs[chat_id].append("playoff")
        return await fetch_and_render(
            chat_id=chat_id,
            model=PlayoffModel,
            url=UrlBuilder.build_url("playoff"),
            cache_key="playoff"
        )

    @classmethod
    async def _playoff_series(cls, chat_id: int, chunks: list[str]):
        breadcrumbs[chat_id].append("playoff_series")
        series_letter = chunks[2]
        return await fetch_and_render(
            chat_id=chat_id,
            model=PlayoffSeriesModel,
            url=UrlBuilder.build_url("playoff_series", series_letter),
            cache_key=f"playoff_series_{series_letter}",
            render_kwargs={"series_letter": series_letter}
        )
