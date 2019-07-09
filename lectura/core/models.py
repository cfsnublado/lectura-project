import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class UserstampModel(models.Model):
    '''
    A model that records which user created it and which
    user last updated it.
    '''
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name='%(app_label)s_%(class)s_created_objects',
        on_delete=models.SET_NULL
    )
    last_updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name='%(app_label)s_%(class)s_last_updated_objects',
        on_delete=models.SET_NULL
    )

    class Meta:
        abstract = True


class SerializeModel(models.Model):

    serializer = None

    class Meta:
        abstract = True

    def get_serializer(self):
        if self.serializer is not None:
            return self.serializer(self)
        else:
            return self.serializer

    def serialize(self):
        if self.serializer is not None:
            return self.get_serializer().data


class TimestampModel(models.Model):
    date_created = models.DateTimeField(
        verbose_name=_('label_date_created'),
        default=timezone.now,
        editable=False
    )
    date_updated = models.DateTimeField(
        verbose_name=_('label_date_updated'),
        auto_now=True,
        editable=False
    )

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    '''
    A model whose id is a generated uuid.
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
