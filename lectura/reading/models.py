from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import (
    SerializeModel,
    SlugifyModel, TimestampModel
)
from .managers import ReadingManager, ProjectManager


# Abstract models
class ProjectContentModel(models.Model):

    class Meta:
        abstract = True

    def get_project(self):
        raise NotImplementedError('Method get_project needs to be implemented.')


# Concrete models

class Project(
    TimestampModel, SlugifyModel,
    SerializeModel
):
    unique_slug = False
    slug_value_field_name = 'name'
    slug_max_iterations = 500

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(app_label)s_%(class)s',
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

    objects = ProjectManager()

    class Meta:
        unique_together = ('owner', 'name')
        verbose_name = _('label_project')
        verbose_name_plural = _('label_project_plural')

    def __str__(self):
        return self.name

    def get_serializer(self):
        from .serializers import ProjectSerializer
        return ProjectSerializer


class Reading(
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
        Project,
        related_name='readings',
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
    audio_url = models.URLField(
        verbose_name=_('label_audio_url'),
        blank=True
    )

    objects = ReadingManager()

    class Meta:
        unique_together = ('project', 'name')
        verbose_name = _('label_reading')
        verbose_name_plural = _('label_reading_plural')

    def __str__(self):
        return self.name

    def get_serializer(self):
        from .serializers import ReadingSerializer
        return ReadingSerializer

    def get_project(self):
        return self.project
