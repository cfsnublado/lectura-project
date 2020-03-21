from rest_framework.permissions import BasePermission

from reading.permissions import (
    can_edit_post, is_project_member,
    is_project_admin, is_project_owner
)


class PostEditPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        if view.action not in ['retrieve', 'list']:
            return user.is_superuser or can_edit_post(user, obj)
        else:
            return True


class ProjectMemberPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        if view.action not in ['retrieve', 'list']:
            return user.is_superuser or is_project_member(user, obj)
        else:
            return True


class ProjectOwnerPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        if view.action not in ['retrieve', 'list']:
            return user.is_superuser or is_project_owner(user, obj)
        else:
            return True


class ProjectAdminPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        if view.action not in ['retrieve', 'list']:
            return user.is_superuser or is_project_admin(user, obj)
        else:
            return True
