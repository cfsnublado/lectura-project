from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView, TemplateView, UpdateView
)
from core.views import (
    MessageMixin, ObjectSessionMixin
)
from django.urls import reverse

from ..forms import ProjectCreateForm, ProjectUpdateForm
from ..models import Project, ProjectMember
from .views_mixins import (
    ProjectEditMixin, ProjectSessionMixin
)

APP_NAME = apps.get_app_config("reading").name


class ProjectsView(
    LoginRequiredMixin, ObjectSessionMixin,
    TemplateView
):
    template_name = "{0}/auth/projects.html".format(APP_NAME)


class ProjectCreateView(
    LoginRequiredMixin, ObjectSessionMixin,
    MessageMixin, CreateView
):
    model = Project
    form_class = ProjectCreateForm
    template_name = "{0}/auth/project_create.html".format(APP_NAME)

    def get_form_kwargs(self):
        kwargs = super(ProjectCreateView, self).get_form_kwargs()
        kwargs["owner"] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse(
            "reading:project",
            kwargs={
                "project_pk": self.object.id,
                "project_slug": self.object.slug
            }
        )


class ProjectUpdateView(
    LoginRequiredMixin, ProjectEditMixin,
    ProjectSessionMixin,
    MessageMixin, UpdateView
):
    model = Project
    form_class = ProjectUpdateForm
    template_name = "{0}/auth/project_update.html".format(APP_NAME)

    def get_object(self, **kwargs):
        return self.project

    def get_success_url(self):
        return reverse(
            "reading:project_update",
            kwargs={
                "project_pk": self.object.pk,
                "project_slug": self.object.slug
            }
        )
