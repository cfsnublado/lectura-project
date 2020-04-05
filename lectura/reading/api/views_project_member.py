from rest_framework.generics import get_object_or_404
from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin,
    RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.viewsets import (
    GenericViewSet
)

from core.api.permissions import ReadPermission
from core.api.views_api import APIDefaultsMixin
from ..models import Project, ProjectMember
from ..serializers import ProjectMemberSerializer
from .pagination import SmallPagination
from .permissions import ProjectOwnerPermission


class ProjectMemberViewSet(
    APIDefaultsMixin, RetrieveModelMixin, UpdateModelMixin,
    DestroyModelMixin, ListModelMixin, GenericViewSet
):
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    serializer_class = ProjectMemberSerializer
    queryset = ProjectMember.objects.select_related(
        'project', 'member', 'member__profile'
    ).order_by('-date_created')
    permission_classes = [ReadPermission]
    pagination_class = SmallPagination

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj


class NestedProjectMemberViewSet(
    APIDefaultsMixin, CreateModelMixin,
    ListModelMixin, GenericViewSet
):
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    queryset = ProjectMember.objects.select_related(
        'project', 'member', 'member__profile'
    ).order_by('-date_created')
    serializer_class = ProjectMemberSerializer
    project = None
    permission_classes = [ReadPermission, ProjectOwnerPermission]
    pagination_class = SmallPagination

    def get_project(self, project_pk=None):
        if not self.project:
            self.project = get_object_or_404(Project, id=project_pk)
        return self.project

    def get_queryset(self):
        return self.queryset.filter(project_id=self.kwargs['project_pk'])

    def create(self, request, *args, **kwargs):
        self.get_project(project_pk=kwargs['project_pk'])
        self.check_object_permissions(request, self.project)
        return super(NestedProjectMemberViewSet, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(
            member=self.request.user,
            project=self.project
        )

    def list(self, request, *args, **kwargs):
        self.get_project(project_pk=kwargs['project_pk'])
        return super(NestedProjectMemberViewSet, self).list(request, *args, **kwargs)
