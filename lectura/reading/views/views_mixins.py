from django.http import Http404
from django.shortcuts import get_object_or_404

from core.views import CachedObjectMixin, ObjectSessionMixin, PermissionMixin
from ..models import Post, ReadingProject
from ..permissions import (
    can_create_post, can_edit_post, is_project_admin, is_project_editor,
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
                ReadingProject.objects.select_related('owner'),
                id=kwargs[self.project_id]
            )
        elif self.project_slug in kwargs:
            self.project = get_object_or_404(
                ReadingProject.objects.select_related('owner'),
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


# Project permission mixins are tu be used with ProjectMixin.
class ProjectMemberPermissionMixin(PermissionMixin):

    def check_permission(self):
        return is_project_member(self.request.user, self.project)


class ProjectOwnerPermissionMixin(PermissionMixin):

    def check_permission(self):
        return is_project_owner(self.request.user, self.project)


class ProjectAdminPermissionMixin(PermissionMixin):

    def check_permission(self):
        is_project_admin(self.request.user, self.project)


class ProjectEditorPermissionMixin(PermissionMixin):

    def check_permission(self):
        return is_project_editor(self.request.user, self.project)


class ProjectSessionMixin(ObjectSessionMixin):
    session_obj = 'project'
    session_obj_attrs = ['id', 'name', 'slug']


class PostMixin(CachedObjectMixin):
    post_id = 'post_pk'
    post_slug = 'post_slug'
    project = None
    post_obj = None
    post_admin = False

    def dispatch(self, request, *args, **kwargs):
        self.get_post(request, *args, **kwargs)
        if request.user.is_authenticated:
            self.post_admin = can_edit_post(request.user, self.post_obj)
        return super(PostMixin, self).dispatch(request, *args, **kwargs)

    def get_post(self, request, *args, **kwargs):
        if self.post_id in kwargs:
            self.post_obj = get_object_or_404(
                Post.objects.select_related('creator', 'project'),
                id=kwargs[self.post_id]
            )
        elif self.post_slug in kwargs:
            self.post_obj = get_object_or_404(
                Post.objects.select_related('creator', 'project'),
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
        context['post_admin'] = self.post_admin

        return context


# Post permission mixins are tu be used with PosttMixin.
class PostCreatePermissionMixin(PermissionMixin):

    def check_permission(self):
        return can_create_post(self.request.user, self.project)


class PostEditPermissionMixin(PermissionMixin):

    def check_permission(self):
        return self.post_admin or can_edit_post(self.request.user, self.post_obj)


class PostSessionMixin(ObjectSessionMixin):
    session_obj = 'post_obj'
    session_obj_attrs = ['id', 'name', 'slug']
