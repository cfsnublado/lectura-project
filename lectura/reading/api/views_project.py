from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from core.api.views_api import APIDefaultsMixin
from core.api.permissions import ReadPermission
from core.utils import str_to_bool
from ..serializers import ProjectSerializer
from ..models import Project
from ..utils import import_project
from .pagination import SmallPagination
from .permissions import ProjectOwnerPermission


class ProjectViewSet(APIDefaultsMixin, ModelViewSet):
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    serializer_class = ProjectSerializer
    queryset = Project.objects.order_by('date_created')
    permission_classes = [ReadPermission, ProjectOwnerPermission]
    pagination_class = SmallPagination

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)

        return obj

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        auth = self.request.query_params.get('auth', None)
        if str_to_bool(auth):
            self.queryset = self.queryset.filter(owner=request.user)
        return super(ProjectViewSet, self).list(request, *args, **kwargs)


class ProjectImportView(APIDefaultsMixin, APIView):

    def post(self, request, *args, **kwargs):
        data = request.data
        import_project(data, request.user)

        return Response(data={'success_msg': 'OK!'}, status=status.HTTP_201_CREATED)
