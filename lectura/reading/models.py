from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import (
    ProjectModel, ProjectContentModel, ProjectMemberModel,
    SerializeModel, SlugifyModel, TimestampModel
)
from .managers import PostManager, ReadingProjectManager


class ReadingProject(ProjectModel):

    objects = ReadingProjectManager()

    def get_serializer(self):
        from .serializers import ReadingProjectSerializer
        return ReadingProjectSerializer


class ReadingProjectMember(ProjectMemberModel):

    project = models.ForeignKey(
        ReadingProject,
        related_name='project_team_members',
        on_delete=models.CASCADE
    )


class Post(
    TimestampModel, SlugifyModel, SerializeModel,
    ProjectContentModel
):
    unique_slug = False
    slug_value_field_name = 'name'
    slug_max_iterations = 500

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(app_label)s_%(class)s',
        on_delete=models.CASCADE
    )
    project = models.ForeignKey(
        ReadingProject,
        related_name='posts',
        on_delete=models.CASCADE
    )
    name = models.CharField(
        verbose_name=_('label_name'),
        max_length=255,
    )
    description = models.TextField(
        verbose_name=_('label_description'),
        blank=True
    )
    content = models.TextField(
        verbose_name=_('label_content'),
    )

    objects = PostManager()

    def get_serializer(self):
        from .serializers import PostSerializer
        return PostSerializer

    def get_project(self):
        return self.project

    class Meta:
        verbose_name = _('label_post')
        verbose_name_plural = _('label_post_plural')
        unique_together = ('project', 'name')

    def __str__(self):
        return self.name


class Audio(
    TimestampModel, SlugifyModel,
    SerializeModel
):
    unique_slug = False
    slug_value_field_name = 'name'
    slug_max_iterations = 500

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(app_label)s_%(class)s',
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        related_name='audios',
        on_delete=models.CASCADE
    )
    name = models.CharField(
        verbose_name=_('label_name'),
        max_length=255,
    )
    url = models.URLField(
        verbose_name=_('label_url')
    )
