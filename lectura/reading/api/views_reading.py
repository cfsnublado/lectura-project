from rest_framework.generics import get_object_or_404
from rest_framework.mixins import (
    DestroyModelMixin, ListModelMixin,
    RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.viewsets import (
    GenericViewSet
)

from core.api.views_api import APIDefaultsMixin
from ..models import Reading
from ..serializers import (
    ReadingSerializer
)
from .pagination import SmallPagination
from .permissions import (
    ReadingCreatorPermission, ReadPermission
)


class ReadingViewSet(
    APIDefaultsMixin, RetrieveModelMixin, UpdateModelMixin,
    DestroyModelMixin, ListModelMixin, GenericViewSet
):
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    serializer_class = ReadingSerializer
    queryset = Reading.objects.select_related('project')
    permission_classes = [ReadPermission, ReadingCreatorPermission]
    pagination_class = SmallPagination

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)

        return obj
