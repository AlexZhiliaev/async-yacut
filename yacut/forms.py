from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Optional

from .validators import validate_custom_id, validate_url


class URLMapForm(FlaskForm):
    """Форма для создания короткой ссылки."""

    original_link = StringField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле')],
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Optional()],
    )
    submit = SubmitField('Создать')

    def validate_original_link(self, field):
        """Проверяет валидность URL."""
        validate_url(field.data)

    def validate_custom_id(self, field):
        """Проверяет валидность пользовательского короткого идентификатора."""
        if field.data:
            validate_custom_id(field.data)


class FileUploadForm(FlaskForm):
    """Форма для загрузки файлов на Яндекс.Диск."""

    files = MultipleFileField(
        'Выберите файлы',
        validators=[DataRequired(message='Выберите хотя бы один файл')],
    )
    submit = SubmitField('Загрузить')