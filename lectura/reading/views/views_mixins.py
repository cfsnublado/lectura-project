from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404

from core.views import CachedObjectMixin, ObjectSessionMixin
from ..models import Entry, Project


class PermissionMixin(object):
    superuser_override = True

    def dispatch(self, request, *args, **kwargs):
        has_permission = self.check_permission()

        if not has_permission:
            raise PermissionDenied

        return super(PermissionMixin, self).dispatch(request, *args, **kwargs)

    def check_permission(self, *args, **kwargs):
        raise NotImplementedError('Method check_permission needs to be implemented.')


class ProjectPermissionMixin(PermissionMixin):

    def check_permission(self):
        has_permission = False

        if self.superuser_override:
            if self.request.user.is_superuser or self.project.owner_id == self.request.user.id:
                has_permission = True
        else:
            if self.project.owner_id == self.request.user.id:
                has_permission = True

        return has_permission


class ProjectSessionMixin(ObjectSessionMixin):
    session_obj = 'project'
    session_obj_attrs = ['id', 'name', 'slug']


class ProjectMixin(CachedObjectMixin):
    project_id = 'project_pk'
    project_slug = 'project_slug'
    project = None

    def dispatch(self, request, *args, **kwargs):
        self.get_project(request, *args, **kwargs)
        return super(ProjectMixin, self).dispatch(request, *args, **kwargs)

    def get_project(self, request, *args, **kwargs):
        if self.project_id in kwargs:
            self.project = get_object_or_404(
                Project.objects.prefetch_related('owner'),
                id=kwargs[self.project_id]
            )
        elif self.project_slug in kwargs:
            self.project = get_object_or_404(
                Project.objects.prefetch_related('owner'),
                slug=kwargs[self.project_slug]
            )
        else:
            obj = self.get_object()
            if hasattr(obj, 'project_id'):
                self.project = obj.project
            elif isinstance(obj, Project):
                self.project = obj
            else:
                raise Http404('Project not found.')

    def get_context_data(self, **kwargs):
        context = super(ProjectMixin, self).get_context_data(**kwargs)
        context['project'] = self.project

        return context


class EntryPermissionMixin(PermissionMixin):

    def check_permission(self):
        has_permission = False

        if self.superuser_override:
            if self.request.user.is_superuser or self.entry.creator_id == self.request.user.id:
                has_permission = True
        else:
            if self.entry.creator_id == self.request.user.id:
                has_permission = True

        return has_permission


class EntrySessionMixin(ObjectSessionMixin):
    session_obj = 'entry'
    session_obj_attrs = ['id', 'name', 'slug']


class EntryMixin(CachedObjectMixin):
    entry_id = 'entry_pk'
    entry_slug = 'entry_slug'
    project = None
    entry = None
    entry_admin = False

    def dispatch(self, request, *args, **kwargs):
        self.get_entry(request, *args, **kwargs)

        if request.user.is_superuser or request.user.id == self.entry.creator_id:
            self.entry_admin = True

        return super(EntryMixin, self).dispatch(request, *args, **kwargs)

    def get_entry(self, request, *args, **kwargs):
        if self.entry_id in kwargs:
            self.entry = get_object_or_404(
                Entry.objects.prefetch_related('creator', 'project'),
                id=kwargs[self.entry_id]
            )
        elif self.entry_slug in kwargs:
            self.entry = get_object_or_404(
                Entry.objects.prefetch_related('creator', 'project'),
                slug=kwargs[self.entry_slug]
            )
        else:
            obj = self.get_object()

            if hasattr(obj, 'entry_id'):
                self.entry = obj.entry
            elif isinstance(obj, Entry):
                    self.entry = obj
            else:
                raise Http404('Entry not found.')

        self.project = self.entry.project

    def get_context_data(self, **kwargs):
        context = super(EntryMixin, self).get_context_data(**kwargs)
        context['project'] = self.project
        context['entry'] = self.entry
        context['entry_admin'] = self.entry_admin

        return context
