from django.apps import apps
from django.views.generic import TemplateView

from ..models import PostAudio
from .views_mixins import (
    PostViewMixin, PostSessionMixin
)

APP_NAME = apps.get_app_config('reading').name


class PostView(
    PostViewMixin, PostSessionMixin,
    TemplateView
):
    template_name = '{0}/post.html'.format(APP_NAME)

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        has_audio = PostAudio.objects.filter(
            post_id=self.post_obj.id
        ).exists()
        context['has_post_audio'] = has_audio
        return context


class PostAudiosView(
    PostViewMixin, PostSessionMixin,
    TemplateView
):
    template_name = '{0}/post_audios.html'.format(APP_NAME)
