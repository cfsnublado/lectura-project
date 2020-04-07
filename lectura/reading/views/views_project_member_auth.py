from django.apps import apps
from django.views.generic import TemplateView

from .views_mixins import ProjectViewMixin, ProjectSessionMixin

APP_NAME = apps.get_app_config('reading').name


class ProjectMembersView(
    ProjectViewMixin, ProjectSessionMixin,
    TemplateView
):
    template_name = '{0}/auth/project_members.html'.format(APP_NAME)
