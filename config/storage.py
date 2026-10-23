from django.conf import settings
from django.contrib.staticfiles.storage import StaticFilesStorage


class VersionedStaticFilesStorage(StaticFilesStorage):
    """
    Добавляет ?v=<FRONTEND_VERSION> ко всем ссылкам {% static %}.
    nginx кэширует статику как immutable, поэтому при смене версии
    браузер видит новый URL и заново скачивает CSS/JS.
    """

    def url(self, name):
        url = super().url(name)
        version = settings.FRONTEND_VERSION
        if not version:
            return url
        separator = '&' if '?' in url else '?'
        return f'{url}{separator}v={version}'
