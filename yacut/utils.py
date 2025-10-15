import random

from .constants import SHORT_ID_CHARS, SHORT_ID_LENGTH
from .models import URLMap


def get_unique_short_id(
        chars: str = SHORT_ID_CHARS,
        length: int = SHORT_ID_LENGTH,
):
    """Генерирует уникальный короткий идентификатор заданной длины."""
    while True:
        short_id = ''.join(random.choices(chars, k=length))
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id
