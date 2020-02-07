from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from core.api.views_api import APIDefaultsMixin
from core.api.permissions import ReadPermission
from ..serializers import ReadingProjectSerializer
from ..models import ReadingProject
from ..utils import import_project
from .pagination import SmallPagination
from .permissions import ProjectOwnerPermission


class ProjectViewSet(APIDefaultsMixin, ModelViewSet):
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    serializer_class = ReadingProjectSerializer
    queryset = ReadingProject.objects.all()
    permission_classes = [ReadPermission, ProjectOwnerPermission]
    pagination_class = SmallPagination

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)

        return obj

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProjectImportView(APIDefaultsMixin, APIView):

    def post(self, request, *args, **kwargs):
        data = request.data
        import_project(data, request.user)

        return Response(data={'success_msg': 'OK!'}, status=status.HTTP_201_CREATED)
