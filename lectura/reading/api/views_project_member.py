from rest_framework.generics import get_object_or_404
from rest_framework.mixins import (
    DestroyModelMixin, ListModelMixin,
    RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.viewsets import (
    GenericViewSet
)

from core.api.permissions import ReadPermission
from core.api.views_api import APIDefaultsMixin
from ..models import ProjectMember
from ..serializers import ProjectMemberSerializer
from .pagination import SmallPagination


class ProjectMemberViewSet(
    APIDefaultsMixin, RetrieveModelMixin, UpdateModelMixin,
    DestroyModelMixin, ListModelMixin, GenericViewSet
):
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    serializer_class = ProjectMemberSerializer
    queryset = ProjectMember.objects.select_related('project', 'member').order_by('date_created')
    permission_classes = [ReadPermission]
    pagination_class = SmallPagination

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj
