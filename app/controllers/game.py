import logging

from app.controllers.start import breadcrumbs
from app.models.game_summary import GameSummaryModel
from app.utils.api_fetcher import fetch_and_render
from app.utils.urls import UrlBuilder

logger = logging.getLogger("nhlapi.bot")


class GameSummaryController:
    @classmethod
    async def handler(cls, chat_id: int, query: str):
        chunks = query.split("_")

        logger.info(f"User from chat id '{chat_id}' triggered callback with data: {query}")

        return await cls._game_summary(chat_id, chunks)

    @classmethod
    async def _game_summary(cls, chat_id: int, chunks: list[str]):
        breadcrumbs[chat_id].append("game_summary")
        return await fetch_and_render(
            chat_id=chat_id,
            model=GameSummaryModel,
            url=UrlBuilder.build_url("game_summary", chunks[1]),
            cache_key=f"game_{chunks[1]}"
        )
