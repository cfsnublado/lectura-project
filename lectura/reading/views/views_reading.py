from django.apps import apps
from django.views.generic import TemplateView

from .views_mixins import (
    ReadingMixin, ReadingSessionMixin
)

APP_NAME = apps.get_app_config('reading').name


class ReadingView(
    ReadingMixin, ReadingSessionMixin,
    TemplateView
):
    template_name = '{0}/reading.html'.format(APP_NAME)
