from appconf import AppConf

from django.conf import settings


class ReadingConf(AppConf):
    URL_PREFIX = 'reading'
