import logging
from logging.handlers import RotatingFileHandler


class ExcludeTelegramRequestsFilter(logging.Filter):
    def __init__(self, excluded_keywords=None):
        super().__init__()
        self.excluded_keywords = excluded_keywords or []

    def filter(self, record):
        return not any(keyword in record.getMessage() for keyword in self.excluded_keywords)


def setup_logger(name: str, log_file: str = "bot.log", level: int = logging.INFO) -> logging.Logger:
    """
    Настройка и создание логгера.

    :param name: Имя логгера.
    :param log_file: Имя файла для записи логов.
    :param level: Уровень логирования.
    :return: Экземпляр логгера.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(log_format)

    # Обработчик для записи в файл с ротацией
    file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=2)
    file_handler.setFormatter(formatter)

    # Обработчик для вывода в консоль
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Добавляем обработчики к логгеру
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    exclude_filter = ExcludeTelegramRequestsFilter(["getUpdates", "getMe", "deleteWebhook"])
    for handler in logger.handlers:
        handler.addFilter(exclude_filter)

    return logger