from django.utils.translation import ugettext_lazy as _

from core.forms import BaseModelForm
from .models import (
    Reading
)


class ReadingForm(BaseModelForm):

    class Meta:
        abstract = True
        fields = ['name', 'description', 'audio_url', 'content']
        error_messages = {
            'name': {
                'required': _('validation_field_required'),
                'unique': _('validation_field_unique'),
            }
        }


class ReadingCreateForm(ReadingForm):

    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project', None)
        self.creator = kwargs.pop('creator', None)

        super(ReadingCreateForm, self).__init__(*args, **kwargs)

        if not self.project:
            raise ValueError(_('validation_project_required'))

        if not self.creator:
            raise ValueError(_('validation_creator_required'))

        self.instance.project = self.project
        self.instance.creator = self.creator

    class Meta(ReadingForm.Meta):
        model = Reading


class ReadingUpdateForm(ReadingForm):

    class Meta(ReadingForm.Meta):
        model = Reading
