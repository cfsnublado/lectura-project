from django.apps import apps
from django.views.generic import TemplateView

from core.views import (
    ObjectSessionMixin
)
from .views_mixins import ProjectMixin, ProjectSessionMixin

APP_NAME = apps.get_app_config('reading').name


class ProjectsView(ObjectSessionMixin, TemplateView):
    template_name = '{0}/projects.html'.format(APP_NAME)


class ProjectView(
    ProjectMixin, ProjectSessionMixin,
    TemplateView
):
    template_name = '{0}/project.html'.format(APP_NAME)

