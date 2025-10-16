from http import HTTPStatus

from flask import jsonify, request
from wtforms import ValidationError

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .validators import validate_custom_id, validate_url


@app.route('/api/id/', methods=['POST'])
def create_id():
    """Создает новую короткую ссылку."""
    if not request.get_data():
        raise InvalidAPIUsage(
            'Отсутствует тело запроса',
            HTTPStatus.BAD_REQUEST,
        )
    data = request.get_json()
    if 'url' not in data:
        raise InvalidAPIUsage(
            '"url" является обязательным полем!',
            HTTPStatus.BAD_REQUEST,
        )

    try:
        url_map = URLMap.create(
            original_url=data['url'],
            custom_id=data.get('custom_id'),
            url_validator=validate_url,
            custom_id_validator=validate_custom_id,
        )
        return jsonify(url_map.to_dict()), HTTPStatus.CREATED
    except ValidationError as e:
        raise InvalidAPIUsage(str(e), HTTPStatus.BAD_REQUEST)


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    """Возвращает оригинальную ссылку по короткому идентификатору."""
    url_map = URLMap.get_by_short_id(short_id)
    if not url_map:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original})