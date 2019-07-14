from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView, UpdateView
)

from core.views import (
    MessageMixin,
)
from django.urls import reverse

from ..forms import EntryCreateForm, EntryUpdateForm
from ..models import Entry
from .views_mixins import (
    EntryMixin, EntryPermissionMixin, EntrySessionMixin,
    ProjectMixin, ProjectSessionMixin
)

APP_NAME = apps.get_app_config('reading').name


class EntryCreateView(
    LoginRequiredMixin, ProjectMixin,
    ProjectSessionMixin, MessageMixin, CreateView
):
    model = Entry
    form_class = EntryCreateForm
    template_name = '{0}/auth/entry_create.html'.format(APP_NAME)

    def get_form_kwargs(self):
        kwargs = super(EntryCreateView, self).get_form_kwargs()
        kwargs['project'] = self.project
        kwargs['creator'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse(
            'reading:entry_update',
            kwargs={
                'entry_pk': self.object.pk,
                'entry_slug': self.object.slug
            }
        )


class EntryUpdateView(
    LoginRequiredMixin, EntryMixin,
    EntrySessionMixin, EntryPermissionMixin,
    MessageMixin, UpdateView
):
    model = Entry
    form_class = EntryUpdateForm
    template_name = '{0}/auth/entry_update.html'.format(APP_NAME)

    def get_object(self, **kwargs):
        return self.entry

    def get_success_url(self):
        return reverse(
            'reading:entry_update',
            kwargs={
                'entry_pk': self.object.pk,
                'entry_slug': self.object.slug
            }
        )
