from django.http import Http404
from django.shortcuts import get_object_or_404

from core.views import CachedObjectMixin, ObjectSessionMixin, PermissionMixin
from ..models import Post, ReadingProject
from ..permissions import (
    can_create_post, is_project_admin, is_project_editor,
    is_project_member, is_project_owner
)


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
                ReadingProject.objects.prefetch_related('owner'),
                id=kwargs[self.project_id]
            )
        elif self.project_slug in kwargs:
            self.project = get_object_or_404(
                ReadingProject.objects.prefetch_related('owner'),
                slug=kwargs[self.project_slug]
            )
        else:
            obj = self.get_object()
            if hasattr(obj, 'project_id'):
                self.project = obj.project
            elif isinstance(obj, ReadingProject):
                self.project = obj
            else:
                raise Http404('Project not found.')

    def get_context_data(self, **kwargs):
        context = super(ProjectMixin, self).get_context_data(**kwargs)
        context['project'] = self.project

        return context


class ProjectMemberPermissionMixin(PermissionMixin):
    """
    To be used in conjunction with ProjectMixin
    """

    def check_permission(self):
        """Owner or project member"""
        user = self.request.user
        return is_project_owner(user, self.project) or is_project_member(user, self.project)


class ProjectOwnerPermissionMixin(PermissionMixin):
    def check_permission(self):
        """ Project owner"""
        return is_project_owner(self.request.user, self.project)


class ProjectAdminPermissionMixin(PermissionMixin):
    def check_permission(self):
        user = self.request.user
        return is_project_owner(user, self.project) or is_project_admin(user, self.project)


class ProjectEditorPermissionMixin(PermissionMixin):
    def check_permission(self):
        user = self.request.user
        return is_project_owner(user, self.project) or is_project_editor(user, self.project)


class ProjectSessionMixin(ObjectSessionMixin):
    session_obj = 'project'
    session_obj_attrs = ['id', 'name', 'slug']


class PostMixin(CachedObjectMixin):
    post_id = 'post_pk'
    post_slug = 'post_slug'
    project = None
    post_obj = None

    def dispatch(self, request, *args, **kwargs):
        self.get_post(request, *args, **kwargs)

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

        self.project = self.post_obj.project

    def get_context_data(self, **kwargs):
        context = super(PostMixin, self).get_context_data(**kwargs)
        context['project'] = self.project
        context['post'] = self.post_obj

        return context


class PostCreatePermissionMixin(PermissionMixin):
    """
    This is to be used with PostMixin.
    """

    def check_permission(self):
        user = self.request.user
        return can_create_post(user, self.project)


class PostSessionMixin(ObjectSessionMixin):
    session_obj = 'post_obj'
    session_obj_attrs = ['id', 'name', 'slug']
