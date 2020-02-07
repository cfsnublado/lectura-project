from core.api.permissions import (
    CreatorPermission, OwnerPermission
)


class ProjectOwnerPermission(OwnerPermission):
    pass


class PostCreatorPermission(CreatorPermission):
    pass
