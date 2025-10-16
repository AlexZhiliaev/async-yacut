from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Optional


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


class FileUploadForm(FlaskForm):
    """Форма для загрузки файлов на Яндекс.Диск."""

    files = MultipleFileField(
        'Выберите файлы',
        validators=[DataRequired(message='Выберите хотя бы один файл')],
    )
    submit = SubmitField('Загрузить')