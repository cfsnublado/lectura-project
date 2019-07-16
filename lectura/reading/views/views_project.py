from django.apps import apps
from django.views.generic import TemplateView

from core.views import (
    ObjectSessionMixin
)

APP_NAME = apps.get_app_config('reading').name


class ProjectsView(ObjectSessionMixin, TemplateView):
    template_name = '{0}/projects.html'.format(APP_NAME)
