from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import (
    CreateView, TemplateView, UpdateView
)

from core.views import MessageMixin
from ..forms import (
    ProjectMemberCreateForm,
    ProjectMemberUpdateForm
)
from ..models import ProjectMember
from .views_mixins import (
    ProjectEditMixin, ProjectMemberCreateMixin,
    ProjectMemberEditMixin, ProjectSessionMixin
)

APP_NAME = apps.get_app_config('reading').name


class ProjectMembersView(
    LoginRequiredMixin, ProjectEditMixin,
    ProjectSessionMixin, TemplateView
):
    template_name = '{0}/auth/project_members.html'.format(APP_NAME)


class ProjectMemberCreateView(
    LoginRequiredMixin, ProjectMemberCreateMixin,
    ProjectSessionMixin, MessageMixin, CreateView
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


class ProjectMemberUpdateView(
    LoginRequiredMixin, ProjectMemberEditMixin,
    ProjectSessionMixin,
    MessageMixin, UpdateView
):
    model = ProjectMember
    form_class = ProjectMemberUpdateForm
    template_name = '{0}/auth/project_member_update.html'.format(APP_NAME)

    def get_object(self, **kwargs):
        self.project_member = get_object_or_404(
            ProjectMember.objects.select_related('member', 'project'),
            id=self.kwargs['pk']
        )
        return self.project_member

    def get_success_url(self):
        return reverse(
            'reading:project_members_auth',
            kwargs={
                'project_pk': self.project.id,
                'project_slug': self.project.slug
            }
        )

    def get_context_data(self, **kwargs):
        context = super(ProjectMemberUpdateView, self).get_context_data(**kwargs)
        context['project_member'] = self.project_member
        return context
