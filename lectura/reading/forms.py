from django import forms
from django.utils.translation import ugettext_lazy as _

from core.forms import BaseModelForm
from .models import (
    Post, PostAudio, ReadingProject
)


class ProjectForm(BaseModelForm):

    def full_clean(self):
        super(ProjectForm, self).full_clean()
        try:
            self.instance.validate_unique()
        except forms.ValidationError as e:
            self._update_errors(e)

    class Meta:
        abstract = True
        fields = ['name', 'description']
        error_messages = {
            'name': {
                'required': _('validation_field_required'),
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
        model = ReadingProject


class ProjectUpdateForm(ProjectForm):

    class Meta(ProjectForm.Meta):
        model = ReadingProject


class PostForm(BaseModelForm):

    def full_clean(self):
        super(PostForm, self).full_clean()
        try:
            self.instance.validate_unique()
        except forms.ValidationError as e:
            self._update_errors(e)

    class Meta:
        abstract = True
        fields = ['name', 'description', 'content']
        error_messages = {
            'name': {
                'required': _('validation_field_required'),
            }
        }


class PostAudioForm(BaseModelForm):

    class Meta:
        abstract = True
        fields = ['name', 'audio_url']
        error_messages = {
            'name': {
                'required': _('validation_field_required'),
            },
            'audio_url': {
                'required': _('validation_field_required'),
            }
        }


class PostAudioCreateForm(PostAudioForm):

    def __init__(self, *args, **kwargs):
        self.creator = kwargs.pop('creator', None)
        self.post = kwargs.pop('post', None)

        super(PostAudioCreateForm, self).__init__(*args, **kwargs)

        if not self.creator:
            raise ValueError(_('validation_creator_required'))

        if not self.post:
            raise ValueError(_('validation_post_required'))

        self.instance.creator = self.creator
        self.instance.post = self.post

    class Meta(PostAudioForm.Meta):
        model = PostAudio


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
