import re
from urllib.parse import urlparse

from wtforms import ValidationError

from .constants import RESERVED_SHORT_IDS, SHORT_ID_MAX_LENGTH
from .models import URLMap


def validate_custom_id(custom_id: str):
    """Проверяет валидность пользовательского короткого идентификатора."""
    if len(custom_id) > SHORT_ID_MAX_LENGTH:
        raise ValidationError('Указано недопустимое имя для короткой ссылки')

    if not re.match(r'^[A-Za-z0-9]+$', custom_id):
        raise ValidationError('Указано недопустимое имя для короткой ссылки')

    if custom_id in RESERVED_SHORT_IDS:
        raise ValidationError(
            'Предложенный вариант короткой ссылки уже существует.')

    if URLMap.query.filter_by(short=custom_id).first():
        raise ValidationError(
            'Предложенный вариант короткой ссылки уже существует.')
    return custom_id


def validate_url(url: str):
    """Проверяет валидность URL."""
    result = urlparse(url)
    if not all([result.scheme, result.netloc]):
        raise ValidationError('Некорректный URL')