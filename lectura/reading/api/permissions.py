from rest_framework.permissions import BasePermission

from reading.models import ReadingProjectMember


class PostCreatorPermission(BasePermission):
    '''
    Permission granted to object creator or superuser.
    '''

    def has_object_permission(self, request, view, obj):
        user = request.user

        if view.action not in ['retrieve', 'list']:
            return self.check_creator_permission(user, obj)
        else:
            return True

        return self.check_creator_permission(user, obj)

    def check_creator_permission(self, user, obj):
        return user.is_superuser or obj.can_edit(user)


class ProjectOwnerPermission(BasePermission):
    '''
    Superuser or project owner
    '''

    def has_object_permission(self, request, view, obj):
        user = request.user

        if view.action not in ['retrieve', 'list']:
            return self.check_owner_permission(user, obj)
        else:
            return True

    def check_owner_permission(self, user, obj):
        return user.is_superuser or user.id == obj.owner_id


class ProjectAdminPermission(BasePermission):
    '''
    Superuser, Project owner, or ProjectMember admin
    '''

    def has_object_permission(self, request, view, obj):
        user = request.user

        if view.action not in ['retrieve', 'list']:
            return self.check_admin_permission(user, obj)
        else:
            return True

    def check_admin_permission(self, user, obj):
        admin_access = False

        if user.is_superuser or user.id == obj.owner_id:
            admin_access = True
        else:
            member = self.project.get_member(user)
            if member:
                if member.role >= ReadingProjectMember.ROLE_ADMIN:
                    admin_access = True

        return admin_access
