from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import (
    ProjectModel, ProjectContentModel, ProjectPublishMemberModel,
    SerializeModel, SlugifyModel, TimestampModel
)
from .managers import (
    PostManager, ProjectManager,
    ProjectMemberManager
)


class Project(ProjectModel):
    thumb_url = models.URLField(
        verbose_name=_('label_thumb_url'),
        blank=True
    )
    banner_url = models.URLField(
        verbose_name=_('label_banner_url'),
        blank=True,
        default=settings.USERS_IMAGE_DEFAULT_URL
    )

    objects = ProjectManager()

    def get_serializer(self):
        from .serializers import ProjectSerializer
        return ProjectSerializer

    def get_member(self, user):
        member = None
        try:
            member = ProjectMember.objects.get(project=self, member=user)
        except ProjectMember.DoesNotExist:
            pass
        return member


class ProjectMember(ProjectPublishMemberModel):
    project = models.ForeignKey(
        Project,
        related_name='project_publish_members',
        on_delete=models.CASCADE
    )

    objects = ProjectMemberManager()


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
        Project,
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
    thumb_url = models.URLField(
        verbose_name=_('label_thumb_url'),
        blank=True
    )
    banner_url = models.URLField(
        verbose_name=_('label_banner_url'),
        blank=True
    )

    objects = PostManager()

    class Meta:
        verbose_name = _('label_post')
        verbose_name_plural = _('label_post_plural')
        unique_together = ('project', 'name')

    def __str__(self):
        return self.name

    def get_serializer(self):
        from .serializers import PostSerializer
        return PostSerializer

    def get_project(self):
        return self.project


class PostAudio(
    TimestampModel, SlugifyModel,
    SerializeModel, ProjectContentModel
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
        related_name='post_audios',
        on_delete=models.CASCADE
    )
    name = models.CharField(
        verbose_name=_('label_name'),
        max_length=255,
    )
    audio_url = models.URLField(
        verbose_name=_('label_audio_url')
    )

    def get_project(self):
        return self.post.project
