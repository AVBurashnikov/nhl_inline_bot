import logging
import os
import argparse

from telegram.ext import Application, CallbackQueryHandler, CommandHandler
from dotenv import load_dotenv

from app.controllers.callback_query import CallbackQueryController
from app.controllers.start import StartController
from app.utils.logger import setup_logger


logger = setup_logger("nhlapi.bot")


def load_token_from_env():
    """Загружает токен из переменной окружения."""
    token = os.getenv("TELEGRAM_TOKEN")
    if token is None:
        raise ValueError("TELEGRAM_TOKEN не найден в переменных окружения.")
    return token


def load_token_from_dotenv():
    """Загружает токен из .env файла."""
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    token = os.getenv("TOKEN")
    if token is None:
        raise ValueError("TOKEN не найден в .env файле.")
    return token


def main() -> None:
    """Основной код запуска бота."""

    parser = argparse.ArgumentParser(description="Запуск NHLHelper в режиме dev или prod.")
    parser.add_argument(
        "mode",
        choices=["dev", "prod"],
        help="Режим запуска: 'dev' или 'prod'"
    )
    args = parser.parse_args()

    try:
        if args.mode == "dev":
            token = load_token_from_env()
        else:
            token = load_token_from_dotenv()

        logger.info("Token loaded successfully.")

    except ValueError as e:
        logging.critical("Error loading token.")
        exit(1)

    logger.info("Bot started...")

    try:
        application = Application.builder().token(token).build()

        application.add_handler(CommandHandler("start", StartController.handler))
        application.add_handler(CallbackQueryHandler(CallbackQueryController.handler))

        logger.info("Handlers registered...")
        logger.info("Run polling...")

        application.run_polling()

    except Exception as e:
        logger.critical(f"Bot crashed with error: {e}", exc_info=True)


if __name__ == "__main__":
    main()