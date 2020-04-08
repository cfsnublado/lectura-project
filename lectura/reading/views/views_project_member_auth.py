from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import (
    CreateView, TemplateView
)

from ..forms import ProjectMemberCreateForm
from ..models import ProjectMember
from .views_mixins import (
    ProjectEditMixin, ProjectMemberCreateMixin,
    ProjectSessionMixin
)

APP_NAME = apps.get_app_config('reading').name


class ProjectMembersView(
    LoginRequiredMixin, ProjectEditMixin,
    ProjectSessionMixin, TemplateView
):
    template_name = '{0}/auth/project_members.html'.format(APP_NAME)


class ProjectMemberCreateView(
    LoginRequiredMixin, ProjectMemberCreateMixin,
    ProjectSessionMixin, CreateView
):
    model = ProjectMember
    form_class = ProjectMemberCreateForm
    template_name = '{0}/auth/project_member_create.html'.format(APP_NAME)

    def get_form_kwargs(self):
        kwargs = super(ProjectMemberCreateView, self).get_form_kwargs()
        kwargs['project'] = self.project
        return kwargs

    def get_success_url(self):
        return reverse(
            'reading:project_members_auth',
            kwargs={
                'project_pk': self.project.id,
                'project_slug': self.project.slug
            }
        )
