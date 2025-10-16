import random
from datetime import datetime
from typing import Callable, Optional

from flask import url_for

from . import db
from .constants import (
    REDIRECT_VIEW_NAME,
    SHORT_ID_CHARS,
    SHORT_ID_LENGTH,
    SHORT_ID_MAX_LENGTH,
)


class URLMap(db.Model):
    """Модель для хранения сопоставления коротких и оригинальных ссылок."""

    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    original = db.Column(
        db.Text,
        nullable=False,
    )
    short = db.Column(
        db.String(SHORT_ID_MAX_LENGTH),
        unique=True,
        nullable=False,
    )
    timestamp = db.Column(
        db.DateTime,
        index=True,
        default=datetime.utcnow,
    )

    def to_dict(self):
        """Возвращает данные модели в виде словаря для API."""
        return dict(
            url=self.original,
            short_link=url_for(
                REDIRECT_VIEW_NAME,
                short_id=self.short,
                _external=True,
            ),
        )

    @staticmethod
    def get_unique_short_id(
            chars: str = SHORT_ID_CHARS,
            length: int = SHORT_ID_LENGTH,
    ):
        """Генерирует уникальный короткий идентификатор заданной длины."""
        while True:
            short_id = ''.join(random.choices(chars, k=length))
            if not URLMap.get_by_short_id(short_id):
                return short_id

    @staticmethod
    def create(
            original_url: str,
            custom_id: Optional[str],
            url_validator: Callable[[str], None],
            custom_id_validator: Callable[[str], str],
    ):
        """Создает запись в URLMap с валидацией полей."""
        url_validator(original_url)

        if custom_id:
            short_id = custom_id_validator(custom_id)
        else:
            short_id = URLMap.get_unique_short_id()

        url_map = URLMap(original=original_url, short=short_id)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @staticmethod
    def get_by_short_id(short_id: str):
        """Возвращает URLMap по короткому идентификатору или None."""
        return URLMap.query.filter_by(short=short_id).first()