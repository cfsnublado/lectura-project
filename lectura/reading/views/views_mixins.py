from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404

from core.views import CachedObjectMixin, ObjectSessionMixin, PermissionMixin
from ..models import Post, Project
from ..permissions import (
    can_create_post_audio, can_create_project_member,
    can_delete_project, can_edit_post, can_edit_post_audio,
    can_edit_project, can_edit_project_member,
    is_project_member, is_project_owner
)


class ProjectMixin(CachedObjectMixin, PermissionMixin):
    project_id = 'project_pk'
    project_slug = 'project_slug'
    project = None
    check_access = True
    is_project_member = False

    def dispatch(self, request, *args, **kwargs):
        self.get_project(request, *args, **kwargs)
        if self.check_access:
            if request.user.is_authenticated:
                has_permission = self.check_permission()
                if has_permission:
                    self.is_project_member = True
                else:
                    raise PermissionDenied
            else:
                raise PermissionDenied
        elif request.user.is_authenticated:
            self.is_project_member = is_project_member(request.user, self.project)
        return super(ProjectMixin, self).dispatch(request, *args, **kwargs)

    def get_project(self, request, *args, **kwargs):
        if self.project_id in kwargs:
            self.project = get_object_or_404(
                Project.objects.select_related('owner'),
                id=kwargs[self.project_id]
            )
        elif self.project_slug in kwargs:
            self.project = get_object_or_404(
                Project.objects.select_related('owner'),
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
        context['is_project_owner'] = is_project_owner(self.request.user, self.project)
        context['is_project_member'] = self.is_project_member
        return context

    def check_permission(self):
        return False


class ProjectMemberMixin(ProjectMixin):
    check_access = True

    def check_permission(self):
        return is_project_member(self.request.user, self.project)


class ProjectViewMixin(ProjectMixin):
    check_access = False


class ProjectEditMixin(ProjectMixin):
    check_access = True

    def check_permission(self):
        return can_edit_project(self.request.user, self.project)


class ProjectDeleteMixin(ProjectMixin):
    check_access = True

    def check_permission(self):
        return can_delete_project(self.request.user, self.project)


class ProjectMemberCreateMixin(ProjectMixin):
    check_access = True

    def check_permission(self):
        return can_create_project_member(self.request.user, self.project)


class ProjectMemberEditMixin(ProjectMixin):
    check_access = True

    def check_permission(self):
        return can_edit_project_member(self.request.user, self.project)


class ProjectSessionMixin(ObjectSessionMixin):
    session_obj = 'project'
    session_obj_attrs = ['id', 'name', 'slug']


class PostMixin(CachedObjectMixin, PermissionMixin):
    post_id = 'post_pk'
    post_slug = 'post_slug'
    project = None
    post_obj = None
    check_access = True
    is_post_admin = False

    def dispatch(self, request, *args, **kwargs):
        self.get_post(request, *args, **kwargs)
        if self.check_access:
            if request.user.is_authenticated:
                has_permission = self.check_permission()
                if has_permission:
                    self.is_post_admin = True
                else:
                    raise PermissionDenied
            else:
                raise PermissionDenied
        elif request.user.is_authenticated:
            self.is_post_admin = can_edit_post(request.user, self.post_obj)
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
        context['is_post_admin'] = self.is_post_admin
        context['is_project_owner'] = is_project_owner(self.request.user, self.project)
        return context

    def check_permission(self):
        return False


class PostViewMixin(PostMixin):
    check_access = False


class PostEditMixin(PostMixin):
    check_access = True

    def check_permission(self):
        return can_edit_post(self.request.user, self.post_obj)


class PostDeleteMixin(PostMixin):
    check_access = True

    def check_permission(self):
        return can_edit_post(self.request.user, self.post_obj)


class PostAudioCreateMixin(PostMixin):
    check_access = True

    def check_permission(self):
        return can_create_post_audio(self.request.user, self.post_obj)


class PostAudioEditMixin(PostMixin):
    check_access = True

    def check_permission(self):
        return can_edit_post_audio(self.request.user, self.post_obj)


class PostSessionMixin(ObjectSessionMixin):
    session_obj = 'post_obj'
    session_obj_attrs = ['id', 'name', 'slug']
