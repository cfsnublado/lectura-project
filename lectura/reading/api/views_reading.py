from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin,
    RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import (
    GenericViewSet
)
from rest_framework.views import APIView

from core.api.views_api import APIDefaultsMixin
from ..models import Project, Reading
from ..serializers import (
    ReadingSerializer
)
from .pagination import SmallPagination
from .permissions import (
    ProjectOwnerPermission, ReadingCreatorPermission, ReadPermission
)
from ..utils import (
    export_reading, import_reading
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


class NestedReadingViewSet(
    APIDefaultsMixin, CreateModelMixin,
    ListModelMixin, GenericViewSet
):
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    queryset = Reading.objects.select_related('project')
    serializer_class = ReadingSerializer
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

        return super(NestedReadingViewSet, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(
            creator=self.request.user,
            project=self.project
        )

    def list(self, request, *args, **kwargs):
        self.get_project(project_pk=kwargs['project_pk'])

        return super(NestedReadingViewSet, self).list(request, *args, **kwargs)


class ReadingImportView(APIDefaultsMixin, APIView):

    def post(self, request, *args, **kwargs):
        data = request.data
        import_reading(data, request.user)

        return Response(data={'success_msg': 'OK!'}, status=status.HTTP_201_CREATED)


class ReadingExportView(APIDefaultsMixin, APIView):
    permission_classes = [
        IsAuthenticated, ReadingCreatorPermission
    ]

    def get(self, request, *args, **kwargs):
        reading = self.get_object()
        data = export_reading(request, reading)

        return Response(data=data)

    def get_object(self):
        obj = get_object_or_404(
            Reading.objects.select_related('project'),
            id=self.kwargs['reading_pk']
        )

        self.check_object_permissions(self.request, obj)

        return obj
