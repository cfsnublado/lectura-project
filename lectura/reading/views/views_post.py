from django.apps import apps
from django.views.generic import TemplateView

from .views_mixins import (
    PostMixin, PostSessionMixin
)
from ..models import Audio

APP_NAME = apps.get_app_config('reading').name


class PostView(
    PostMixin, PostSessionMixin,
    TemplateView
):
    template_name = '{0}/post.html'.format(APP_NAME)

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        audios = Audio.objects.filter(post_id=self.post_obj.id)
        if audios:
            context['audio_url'] = audios.all()[0].url
        else:
            context['audio_url'] = None

        return context
