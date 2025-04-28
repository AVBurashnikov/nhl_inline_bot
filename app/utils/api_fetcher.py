import logging
from typing import Optional, Any

import aiohttp
from telegram import InlineKeyboardMarkup
from telegram.error import BadRequest

from app.menu import bot_menu
from app.utils.cache import cache

logger = logging.getLogger("nhlapi.bot")


async def fetch_data(url: str) -> Optional[dict]:
    logger.info(f"Try to get data from {url}.")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                logger.info(f"Data from {url} successfully loaded. Status 200.")
                return await response.json()
            return None


async def handle_api_response(model: Any, url: str) -> None:

    try:
        data = await fetch_data(url)

        if data is None:
            logger.warning("API request or cache returned no data.")
            return

        model_instance = model(**data)
        logger.info(f"Successfully processed and sent message for {model.__name__}.")

        return model_instance

    except BadRequest as e:
        if "Message is not modified" in str(e):
            logger.warning("The message has not been changed.")
        else:
            logger.error(f"Error while editing message: {str(e).lower()}")

    except Exception as e:
        logger.error(f"Error processing API response: {e}", exc_info=True)


async def fetch_and_render(
        chat_id: int,
        model: Any,
        url: str,
        cache_key: str,
        cache_ttl: int = 3600,
        render_kwargs=None,
):
    render_kwargs = render_kwargs or {}
    logger.debug(f"Fetching model '{model.__name__}' for chat '{chat_id}' from URL: {url}")

    message, menu = cache.get_value_or_none(cache_key)

    if message and menu:
        logger.info(f"Data retrieved from cache by key '{cache_key}'.")
        logger.info(f"Successfully rendered response for chat '{chat_id}'")

        return message, menu

    model_instance = await handle_api_response(model, url)

    if model_instance is None:
        logger.error(f"Failed to fetch data for model '{model.__name__}' for chat '{chat_id}'")

        return "Ошибка.", bot_menu.back_menu

    message = model_instance.render_message(**render_kwargs)
    menu = model_instance.render_menu(**render_kwargs)

    cache.set_value(cache_key, (message, menu), cache_ttl)

    logger.info(f"Data is cached by key '{cache_key}'")
    logger.info(f"Cache size: {(cache.size / 1_048_576):.3f} MB.")
    logger.info(f"Successfully rendered response for chat '{chat_id}'")

    return message, menu
