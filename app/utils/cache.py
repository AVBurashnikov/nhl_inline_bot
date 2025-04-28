import sys
import time
import logging


logger = logging.getLogger("nhlapi.bot")


#  TODO: реализовать самостоятельное удаление записи из кеша по истечении времени жизни
class TTLCache:
    def __init__(self):
        self.cache = {}

    def has(self, key):
        if key in self.cache:
            value, timestamp, ttl = self.cache[key]
            if time.time() - timestamp < ttl:
                return True
        return False

    def get_value_or_none(self, key):
        if key in self.cache:
            value, timestamp, ttl = self.cache[key]
            if time.time() - timestamp < ttl:
                return value
            else:
                del self.cache[key]
        return None, None

    def set_value(self, key, value, ttl):
        self.cache[key] = (value, time.time(), ttl)

    # def _is_expired(self, key):
    @property
    def size(self):
        return get_size(self.cache)


def get_size(obj, seen=None):
    """Рекурсивно вычисляет размер объекта в байтах."""
    if seen is None:
        seen = set()

    # Если объект уже был обработан, возвращаем 0
    if id(obj) in seen:
        return 0

    # Добавляем объект в множество обработанных
    seen.add(id(obj))

    # Базовый размер объекта
    size = sys.getsizeof(obj)

    # Если объект является словарем, рекурсивно вычисляем размер его элементов
    if isinstance(obj, dict):
        for key, value in obj.items():
            size += get_size(key, seen)
            size += get_size(value, seen)
    # Если объект является списком, множеством или кортежем, рекурсивно вычисляем размер его элементов
    elif isinstance(obj, (list, tuple, set)):
        for item in obj:
            size += get_size(item, seen)

    return size


cache = TTLCache()
