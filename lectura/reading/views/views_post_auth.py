from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView, UpdateView
)

from core.views import (
    MessageMixin,
)
from django.urls import reverse

from ..forms import (
    PostAudioCreateForm, PostCreateForm,
    PostUpdateForm
)
from ..models import Post, PostAudio
from .views_mixins import (
    PostAudioCreateMixin, PostEditMixin, PostSessionMixin,
    ProjectMemberMixin, ProjectSessionMixin
)

APP_NAME = apps.get_app_config('reading').name


class PostCreateView(
    LoginRequiredMixin, ProjectMemberMixin,
    ProjectSessionMixin, MessageMixin, CreateView
):
    model = Post
    form_class = PostCreateForm
    template_name = '{0}/auth/post_create.html'.format(APP_NAME)

    def get_form_kwargs(self):
        kwargs = super(PostCreateView, self).get_form_kwargs()
        kwargs['project'] = self.project
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
    LoginRequiredMixin, PostEditMixin,
    PostSessionMixin,
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


class PostAudioCreateView(
    LoginRequiredMixin, PostAudioCreateMixin,
    PostSessionMixin,
    MessageMixin, CreateView
):
    model = PostAudio
    form_class = PostAudioCreateForm
    template_name = '{0}/auth/post_audio_create.html'.format(APP_NAME)

    def get_form_kwargs(self):
        kwargs = super(PostAudioCreateView, self).get_form_kwargs()
        kwargs['post'] = self.post_obj
        kwargs['creator'] = self.request.user

        return kwargs

    def get_success_url(self):
        return reverse(
            'reading:post',
            kwargs={
                'post_pk': self.post_obj.pk,
                'post_slug': self.post_obj.slug
            }
        )
