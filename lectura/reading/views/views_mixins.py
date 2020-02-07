from django.http import Http404
from django.shortcuts import get_object_or_404

from core.views import CachedObjectMixin, ObjectSessionMixin, PermissionMixin
from ..models import Post, ReadingProject


class ProjectPermissionMixin(PermissionMixin):

    def check_permission(self):
        has_permission = False

        if self.superuser_override:
            if self.request.user.is_superuser or self.project_obj.owner_id == self.request.user.id:
                has_permission = True
        else:
            if self.project_obj.owner_id == self.request.user.id:
                has_permission = True

        return has_permission


class ProjectSessionMixin(ObjectSessionMixin):
    session_obj = 'project_obj'
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
            self.project_obj = get_object_or_404(
                ReadingProject.objects.prefetch_related('owner'),
                id=kwargs[self.project_id]
            )
        elif self.project_slug in kwargs:
            self.project_obj = get_object_or_404(
                ReadingProject.objects.prefetch_related('owner'),
                slug=kwargs[self.project_slug]
            )
        else:
            obj = self.get_object()
            if hasattr(obj, 'project_id'):
                self.project_obj = obj.project
            elif isinstance(obj, ReadingProject):
                self.project_obj = obj
            else:
                raise Http404('Project not found.')

    def get_context_data(self, **kwargs):
        context = super(ProjectMixin, self).get_context_data(**kwargs)
        context['project'] = self.project_obj

        return context


class PostPermissionMixin(PermissionMixin):

    def check_permission(self):
        has_permission = False

        if self.superuser_override:
            if self.request.user.is_superuser or self.post_obj.creator_id == self.request.user.id:
                has_permission = True
        else:
            if self.post_obj.creator_id == self.request.user.id:
                has_permission = True

        return has_permission


class PostSessionMixin(ObjectSessionMixin):
    session_obj = 'post_obj'
    session_obj_attrs = ['id', 'name', 'slug']


class PostMixin(CachedObjectMixin):
    post_id = 'post_pk'
    post_slug = 'post_slug'
    project = None
    post_obj = None
    post_admin = False

    def dispatch(self, request, *args, **kwargs):
        self.get_post(request, *args, **kwargs)

        user_id = request.user.id

        if request.user.is_superuser or user_id == self.post_obj.creator_id or user_id == self.project_obj.owner_id:
            self.post_admin = True

        return super(PostMixin, self).dispatch(request, *args, **kwargs)

    def get_post(self, request, *args, **kwargs):
        if self.post_id in kwargs:
            self.post_obj = get_object_or_404(
                Post.objects.prefetch_related('creator', 'project'),
                id=kwargs[self.post_id]
            )
        elif self.post_slug in kwargs:
            self.post_obj = get_object_or_404(
                Post.objects.prefetch_related('creator', 'project'),
                slug=kwargs[self.post_slug]
            )
        else:
            obj = self.get_object()

            if hasattr(obj, 'post_id'):
                self.post_obj = obj.post
            elif isinstance(obj, Post):
                    self.post_obj = obj
            else:
                raise Http404('Post not found.')

        self.project_obj = self.post_obj.project

    def get_context_data(self, **kwargs):
        context = super(PostMixin, self).get_context_data(**kwargs)
        context['project'] = self.project_obj
        context['post'] = self.post_obj
        context['post_admin'] = self.post_admin

        return context
