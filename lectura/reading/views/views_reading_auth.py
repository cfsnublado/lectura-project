from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView, UpdateView
)

from core.views import (
    MessageMixin,
)
from django.urls import reverse

from ..forms import ReadingCreateForm, ReadingUpdateForm
from ..models import Reading
from .views_mixins import (
    ReadingMixin, ReadingPermissionMixin, ReadingSessionMixin,
    ProjectMixin, ProjectSessionMixin
)

APP_NAME = apps.get_app_config('reading').name


class ReadingCreateView(
    LoginRequiredMixin, ProjectMixin,
    ProjectSessionMixin, MessageMixin, CreateView
):
    model = Reading
    form_class = ReadingCreateForm
    template_name = '{0}/auth/reading_create.html'.format(APP_NAME)

    def get_form_kwargs(self):
        kwargs = super(ReadingCreateView, self).get_form_kwargs()
        kwargs['project'] = self.project
        kwargs['creator'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse(
            'reading:reading_update',
            kwargs={
                'reading_pk': self.object.pk,
                'reading_slug': self.object.slug
            }
        )


class ReadingUpdateView(
    LoginRequiredMixin, ReadingMixin,
    ReadingSessionMixin, ReadingPermissionMixin,
    MessageMixin, UpdateView
):
    model = Reading
    form_class = ReadingUpdateForm
    template_name = '{0}/auth/reading_update.html'.format(APP_NAME)

    def get_object(self, **kwargs):
        return self.reading

    def get_success_url(self):
        return reverse(
            'reading:reading_update',
            kwargs={
                'reading_pk': self.object.pk,
                'reading_slug': self.object.slug
            }
        )
