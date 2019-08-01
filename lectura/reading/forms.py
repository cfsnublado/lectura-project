from django.utils.translation import ugettext_lazy as _

from core.forms import BaseModelForm
from .models import (
    Project, Post
)


class ProjectForm(BaseModelForm):

    class Meta:
        abstract = True
        fields = ['name', 'description']
        error_messages = {
            'name': {
                'required': _('validation_field_required'),
                'unique': _('validation_field_unique'),
            }
        }


class PostForm(BaseModelForm):

    class Meta:
        abstract = True
        fields = ['name', 'description', 'content', 'audio_url']
        error_messages = {
            'name': {
                'required': _('validation_field_required'),
                'unique': _('validation_field_unique'),
            }
        }


class ProjectCreateForm(ProjectForm):

    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop('owner', None)

        super(ProjectCreateForm, self).__init__(*args, **kwargs)

        if not self.owner:
            raise ValueError(_('validation_owner_required'))

        self.instance.owner = self.owner

    class Meta(ProjectForm.Meta):
        model = Project


class ProjectUpdateForm(ProjectForm):

    class Meta(ProjectForm.Meta):
        model = Project


class PostCreateForm(PostForm):

    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project', None)
        self.creator = kwargs.pop('creator', None)

        super(PostCreateForm, self).__init__(*args, **kwargs)

        if not self.project:
            raise ValueError(_('validation_project_required'))

        if not self.creator:
            raise ValueError(_('validation_creator_required'))

        self.instance.project = self.project
        self.instance.creator = self.creator

    class Meta(PostForm.Meta):
        model = Post


class PostUpdateForm(PostForm):

    class Meta(PostForm.Meta):
        model = Post
