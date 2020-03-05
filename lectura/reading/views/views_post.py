from django.apps import apps
from django.views.generic import TemplateView

from .views_mixins import (
    PostMixin, PostSessionMixin
)
from ..models import PostAudio

APP_NAME = apps.get_app_config('reading').name


class PostView(
    PostMixin, PostSessionMixin,
    TemplateView
):
    template_name = '{0}/post.html'.format(APP_NAME)

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        post_audio_url = self.get_post_audio_url(self.request)
        context['post_audio_url'] = post_audio_url

        return context

    def get_post_audio_url(self, request):
        post_audio_url = None
        post_audio_id = request.GET.get('post_audio_id', None)

        if post_audio_id:
            try:
                post_audio = PostAudio.objects.get(
                    id=post_audio_id,
                    post_id=self.post_obj.id
                )
                post_audio_url = post_audio.url
            except PostAudio.DoesNotExist:
                pass
        else:
            post_audios = PostAudio.objects.filter(post_id=self.post_obj.id)

            if post_audios:
                post_audio_url = post_audios.all()[0].url

        return post_audio_url


class PostAudiosView(
    PostMixin, PostSessionMixin,
    TemplateView
):
    template_name = '{0}/post_audios.html'.format(APP_NAME)
