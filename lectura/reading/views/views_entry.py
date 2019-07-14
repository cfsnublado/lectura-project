from django.apps import apps
from django.views.generic import TemplateView

from .views_mixins import (
    EntryMixin, EntrySessionMixin
)

APP_NAME = apps.get_app_config('reading').name


class EntryView(
    EntryMixin, EntrySessionMixin,
    TemplateView
):
    template_name = '{0}/entry.html'.format(APP_NAME)
