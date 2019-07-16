from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404

from core.views import CachedObjectMixin, ObjectSessionMixin
from ..models import Reading, Project


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


class ReadingPermissionMixin(PermissionMixin):

    def check_permission(self):
        has_permission = False

        if self.superuser_override:
            if self.request.user.is_superuser or self.reading.creator_id == self.request.user.id:
                has_permission = True
        else:
            if self.reading.creator_id == self.request.user.id:
                has_permission = True

        return has_permission


class ReadingSessionMixin(ObjectSessionMixin):
    session_obj = 'reading'
    session_obj_attrs = ['id', 'name', 'slug']


class ReadingMixin(CachedObjectMixin):
    reading_id = 'reading_pk'
    reading_slug = 'reading_slug'
    project = None
    reading = None
    reading_admin = False

    def dispatch(self, request, *args, **kwargs):
        self.get_reading(request, *args, **kwargs)

        if request.user.is_superuser or request.user.id == self.reading.creator_id:
            self.reading_admin = True

        return super(ReadingMixin, self).dispatch(request, *args, **kwargs)

    def get_reading(self, request, *args, **kwargs):
        if self.reading_id in kwargs:
            self.reading = get_object_or_404(
                Reading.objects.prefetch_related('creator', 'project'),
                id=kwargs[self.reading_id]
            )
        elif self.reading_slug in kwargs:
            self.reading = get_object_or_404(
                Reading.objects.prefetch_related('creator', 'project'),
                slug=kwargs[self.reading_slug]
            )
        else:
            obj = self.get_object()

            if hasattr(obj, 'reading_id'):
                self.reading = obj.reading
            elif isinstance(obj, Reading):
                    self.reading = obj
            else:
                raise Http404('Reading not found.')

        self.project = self.reading.project

    def get_context_data(self, **kwargs):
        context = super(ReadingMixin, self).get_context_data(**kwargs)
        context['project'] = self.project
        context['reading'] = self.reading
        context['reading_admin'] = self.reading_admin

        return context
