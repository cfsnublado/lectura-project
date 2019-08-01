from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404

from core.views import CachedObjectMixin, ObjectSessionMixin
from ..models import Post, Project


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


class PostPermissionMixin(PermissionMixin):

    def check_permission(self):
        has_permission = False

        if self.superuser_override:
            if self.request.user.is_superuser or self.post.creator_id == self.request.user.id:
                has_permission = True
        else:
            if self.post.creator_id == self.request.user.id:
                has_permission = True

        return has_permission


class PostSessionMixin(ObjectSessionMixin):
    session_obj = 'post'
    session_obj_attrs = ['id', 'name', 'slug']


class PostMixin(CachedObjectMixin):
    post_id = 'post_pk'
    post_slug = 'post_slug'
    project = None
    post = None
    post_admin = False

    def dispatch(self, request, *args, **kwargs):
        self.get_post(request, *args, **kwargs)

        user_id = request.user.id

        if request.user.is_superuser or user_id == self.post.creator_id or user_id == self.project.owner_id:
            self.post_admin = True

        return super(PostMixin, self).dispatch(request, *args, **kwargs)

    def get_post(self, request, *args, **kwargs):
        if self.post_id in kwargs:
            self.post = get_object_or_404(
                Post.objects.prefetch_related('creator', 'project'),
                id=kwargs[self.post_id]
            )
        elif self.post_slug in kwargs:
            self.post = get_object_or_404(
                Post.objects.prefetch_related('creator', 'project'),
                slug=kwargs[self.post_slug]
            )
        else:
            obj = self.get_object()

            if hasattr(obj, 'post_id'):
                self.post = obj.post
            elif isinstance(obj, Post):
                    self.post = obj
            else:
                raise Http404('Post not found.')

        self.project = self.post.project

    def get_context_data(self, **kwargs):
        context = super(PostMixin, self).get_context_data(**kwargs)
        context['project'] = self.project
        context['post'] = self.post
        context['post_admin'] = self.post_admin

        return context
