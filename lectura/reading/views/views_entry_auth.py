from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView
)

from core.views import (
    MessageMixin,
)
from django.urls import reverse

from ..forms import EntryCreateForm
from ..models import Entry
from .views_mixins import (
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
            'app:home',
        )
