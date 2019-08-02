from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView, UpdateView
)

from core.views import (
    MessageMixin,
)
from django.urls import reverse

from ..forms import PostCreateForm, PostUpdateForm
from ..models import Post
from .views_mixins import (
    PostMixin, PostPermissionMixin, PostSessionMixin,
    ProjectMixin, ProjectSessionMixin
)

APP_NAME = apps.get_app_config('reading').name


class PostCreateView(
    LoginRequiredMixin, ProjectMixin,
    ProjectSessionMixin, MessageMixin, CreateView
):
    model = Post
    form_class = PostCreateForm
    template_name = '{0}/auth/post_create.html'.format(APP_NAME)

    def get_form_kwargs(self):
        kwargs = super(PostCreateView, self).get_form_kwargs()
        kwargs['project'] = self.project_obj
        kwargs['creator'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse(
            'reading:post',
            kwargs={
                'post_pk': self.object.pk,
                'post_slug': self.object.slug
            }
        )


class PostUpdateView(
    LoginRequiredMixin, PostMixin,
    PostSessionMixin, PostPermissionMixin,
    MessageMixin, UpdateView
):
    model = Post
    form_class = PostUpdateForm
    template_name = '{0}/auth/post_update.html'.format(APP_NAME)

    def get_object(self, **kwargs):
        return self.post_obj

    def get_success_url(self):
        return reverse(
            'reading:post',
            kwargs={
                'post_pk': self.object.pk,
                'post_slug': self.object.slug
            }
        )