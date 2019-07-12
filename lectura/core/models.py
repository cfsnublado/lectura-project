import uuid

from django.conf import settings
from django.db import IntegrityError, models
from django.utils import timezone
from django.utils.text import slugify
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


class SlugifyModel(models.Model):
    '''
    Models that inherit from this class get an auto filled slug property based on the models name property.
    Correctly handles duplicate values (slugs are unique), and truncates slug if value too long.
    The following attributes can be overridden on a per model basis:
    * slug_value_field_name - the value to slugify, default 'name'
    * slug_field_name - the field to store the slugified value in, default 'slug'
    * slug_max_iterations - how many iterations to search for an open slug before raising IntegrityError, default 1000
    * slug_separator - the character to put in place of spaces and other non url friendly characters, default '-'
    '''
    slug = models.SlugField(
        verbose_name=_('label_slug'),
        max_length=255,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):

        pk_field_name = self._meta.pk.name
        slug_value_field_name = getattr(self, 'slug_value_field_name', 'name')
        slug_field_name = getattr(self, 'slug_field_name', 'slug')
        slug_max_iterations = getattr(self, 'slug_max_iterations', 1000)
        slug_separator = getattr(self, 'slug_separator', '-')
        unique_slug = getattr(self, 'unique_slug', True)

        if unique_slug:
            # fields, query set, other setup variables
            slug_field = self._meta.get_field(slug_field_name)
            slug_len = slug_field.max_length
            queryset = self.__class__.objects.all()
            # if the pk of the record is set, exclude it from the slug search
            current_pk = getattr(self, pk_field_name)
            if current_pk:
                queryset = queryset.exclude(**{pk_field_name: current_pk})

            # setup the original slug, and make sure it is within the allowed length
            slug = slugify(getattr(self, slug_value_field_name))
            if slug_len:
                slug = slug[:slug_len]
            original_slug = slug

            # iterate until a unique slug is found, or slug_max_iterations
            counter = 2
            while queryset.filter(**{slug_field_name: slug}).count() > 0 and counter < slug_max_iterations:
                slug = original_slug
                suffix = '{0}{1}'.format(slug_separator, counter)
                if slug_len and len(slug) + len(suffix) > slug_len:
                    slug = slug[:slug_len - len(suffix)]
                slug = '{0}{1}'.format(slug, suffix)
                counter += 1

            if counter == slug_max_iterations:
                raise IntegrityError('Unable to locate unique slug')
        else:
            slug = slugify(getattr(self, slug_value_field_name))
        self.slug = slug

        super(SlugifyModel, self).save(*args, **kwargs)
