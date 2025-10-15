import string


# Константы для генерации коротких ссылок.
SHORT_ID_LENGTH = 6
SHORT_ID_MAX_LENGTH = 16
SHORT_ID_CHARS = string.ascii_letters + string.digits

# Зарезервированные имена коротких ссылок.
RESERVED_SHORT_IDS = {'files'}

# Настройки API Яндекс.Диска.
API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
YANDEX_DISK_UPLOAD_URL = 'disk/resources/upload'
YANDEX_DISK_DOWNLOAD_URL = 'disk/resources/download'
REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/{YANDEX_DISK_UPLOAD_URL}'
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/{YANDEX_DISK_DOWNLOAD_URL}'
