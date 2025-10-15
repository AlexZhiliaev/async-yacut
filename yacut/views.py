from flask import flash, redirect, render_template

from . import app, db
from .forms import FileUploadForm, URLMapForm
from .models import URLMap
from .utils import get_unique_short_id
from .yandex_disk import async_upload_files_to_disk


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Главная страница - создание короткой ссылки."""
    form = URLMapForm()
    if form.validate_on_submit():
        original_url = form.original_link.data
        custom_id = form.custom_id.data
        short_id = custom_id.strip() if custom_id else get_unique_short_id()
        url_map = URLMap(original=original_url, short=short_id)
        db.session.add(url_map)
        db.session.commit()
        return render_template('index.html', form=form, short_id=short_id)
    return render_template('index.html', form=form)


@app.route('/files', methods=['GET', 'POST'])
async def upload_files():
    """Страница загрузки файлов."""
    form = FileUploadForm()
    if form.validate_on_submit():
        try:
            file_results = await async_upload_files_to_disk(form.files.data)
            results = []

            for filename, file_url in file_results:
                short_id = get_unique_short_id()
                url_map = URLMap(original=file_url, short=short_id)
                db.session.add(url_map)
                results.append({
                    'filename': filename,
                    'short_id': short_id,
                })

            db.session.commit()
            return render_template('files.html', form=form, results=results)
        except Exception as e:
            flash(f'Ошибка при загрузке файлов: {str(e)}')
    return render_template('files.html', form=form)


@app.route('/<short_id>')
def redirect_to_original(short_id):
    """Перенаправляет по короткой ссылке на оригинальный URL."""
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    response = redirect(url_map.original)
    response.headers['Referrer-Policy'] = 'no-referrer'
    return response