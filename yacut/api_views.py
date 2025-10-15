from flask import jsonify, request
from wtforms import ValidationError

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id
from .validators import validate_custom_id, validate_url


@app.route('/api/id/', methods=['POST'])
def create_id():
    """Создает новую короткую ссылку."""
    if not request.get_data():
        raise InvalidAPIUsage('Отсутствует тело запроса', 400)

    data = request.get_json()

    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!', 400)

    custom_id = data.get('custom_id')

    try:
        validate_url(data['url'])

        if custom_id:
            short_id = validate_custom_id(custom_id)
        else:
            short_id = get_unique_short_id()

        url_map = URLMap(original=data['url'], short=short_id)
        db.session.add(url_map)
        db.session.commit()
        return jsonify(url_map.to_dict()), 201

    except ValidationError as e:
        raise InvalidAPIUsage(str(e), 400)


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    """Возвращает оригинальную ссылку по короткому идентификатору."""
    url_map = URLMap.query.filter_by(short=short_id).first()

    if not url_map:
        raise InvalidAPIUsage('Указанный id не найден', 404)

    return jsonify({'url': url_map.original})