from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ReadingConfig(AppConfig):
    name = 'reading'
    verbose_name = _('label_reading_config')

    def ready(self):
        pass
