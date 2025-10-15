from datetime import datetime

from flask import url_for

from . import db
from .constants import SHORT_ID_MAX_LENGTH


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
                'redirect_to_original',
                short_id=self.short,
                _external=True,
            ),
        )