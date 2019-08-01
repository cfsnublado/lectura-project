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
from ..models import Project, Post
from ..serializers import (
    PostSerializer
)
from .pagination import SmallPagination
from .permissions import (
    ProjectOwnerPermission, PostCreatorPermission, ReadPermission
)
from ..utils import (
    export_post, import_post
)


class PostViewSet(
    APIDefaultsMixin, RetrieveModelMixin, UpdateModelMixin,
    DestroyModelMixin, ListModelMixin, GenericViewSet
):
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    serializer_class = PostSerializer
    queryset = Post.objects.select_related('project')
    permission_classes = [ReadPermission, PostCreatorPermission]
    pagination_class = SmallPagination

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)

        return obj


class NestedPostViewSet(
    APIDefaultsMixin, CreateModelMixin,
    ListModelMixin, GenericViewSet
):
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    queryset = Post.objects.select_related('project')
    serializer_class = PostSerializer
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

        return super(NestedPostViewSet, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(
            creator=self.request.user,
            project=self.project
        )

    def list(self, request, *args, **kwargs):
        self.get_project(project_pk=kwargs['project_pk'])

        return super(NestedPostViewSet, self).list(request, *args, **kwargs)


class PostImportView(APIDefaultsMixin, APIView):

    def post(self, request, *args, **kwargs):
        data = request.data
        import_post(data, request.user)

        return Response(data={'success_msg': 'OK!'}, status=status.HTTP_201_CREATED)


class PostExportView(APIDefaultsMixin, APIView):
    permission_classes = [
        IsAuthenticated, PostCreatorPermission
    ]

    def get(self, request, *args, **kwargs):
        post = self.get_object()
        data = export_post(request, post)

        return Response(data=data)

    def get_object(self):
        obj = get_object_or_404(
            Post.objects.select_related('project'),
            id=self.kwargs['post_pk']
        )

        self.check_object_permissions(self.request, obj)

        return obj
