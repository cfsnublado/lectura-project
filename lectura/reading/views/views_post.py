from django.apps import apps
from django.views.generic import TemplateView

from .views_mixins import (
    PostMixin, PostSessionMixin
)

APP_NAME = apps.get_app_config('reading').name


class PostView(
    PostMixin, PostSessionMixin,
    TemplateView
):
    template_name = '{0}/post.html'.format(APP_NAME)


class PostAudiosView(
    PostMixin, PostSessionMixin,
    TemplateView
):
    template_name = '{0}/post_audios.html'.format(APP_NAME)
