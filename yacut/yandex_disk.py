import asyncio

import aiohttp
from werkzeug.datastructures import FileStorage

from . import app
from .constants import DOWNLOAD_LINK_URL, REQUEST_UPLOAD_URL


async def async_upload_files_to_disk(
        files: list[FileStorage]
) -> list[tuple[str, str]]:
    """Асинхронная загрузка файлов на Яндекс.Диск"""
    disk_token = app.config['DISK_TOKEN']

    if not disk_token:
        raise Exception('Токен Яндекс.Диска не настроен')

    headers = {'Authorization': f'OAuth {disk_token}'}

    async with aiohttp.ClientSession() as session:
        tasks = [
            asyncio.ensure_future(upload_single_file(session, file, headers))
            for file in files
        ]
        return await asyncio.gather(*tasks)


async def upload_single_file(
        session: aiohttp.ClientSession,
        file: FileStorage,
        headers: dict[str, str]
) -> tuple[str, str]:
    """Загрузка одного файла на Яндекс.Диск"""
    filename = file.filename
    params = {
        'path': f'app:/{filename}',
        'overwrite': 'true',
    }

    async with session.get(
        REQUEST_UPLOAD_URL,
        headers=headers,
        params=params,
    ) as response:
        if response.status != 200:
            raise Exception(
                f'Ошибка получения ссылки для загрузки: {response.status}')

        upload_data = await response.json()
        upload_url = upload_data['href']

    file_data = file.read()
    async with session.put(
        upload_url,
        data=file_data,
        headers={'Content-Type': 'application/octet-stream'}
    ) as response:
        if response.status not in (201, 202):
            raise Exception(f'Ошибка загрузки файла: {response.status}')

    async with session.get(
        DOWNLOAD_LINK_URL,
        headers=headers,
        params={'path': f'app:/{filename}'}
    ) as response:
        if response.status != 200:
            raise Exception(
                f'Ошибка получения ссылки для скачивания: {response.status}')
        download_data = await response.json()
        download_url = download_data['href']

    return filename, download_url