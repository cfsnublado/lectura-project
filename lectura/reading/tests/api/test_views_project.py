import json

from rest_framework import status as drf_status
from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin,
    RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from django.contrib.auth import get_user_model
from django.urls import resolve, reverse

from core.api.views_api import APIDefaultsMixin
from reading.api.pagination import SmallPagination
from reading.api.permissions import (
    ProjectOwnerPermission, ReadPermission
)
from reading.api.views_project import (
    ProjectViewSet, ProjectImportView
)
from reading.models import Project
from reading.serializers import ProjectSerializer
from reading.utils import export_project
from .base_test import TestCommon

User = get_user_model()


class ProjectViewSetTest(TestCommon):

    def setUp(self):
        super(ProjectViewSetTest, self).setUp()

        self.project = Project.objects.create(
            owner=self.user,
            name='test project'
        )
        self.user_2 = User.objects.create_user(
            username='abc',
            first_name='Christopher',
            last_name='Sanders',
            email='abc@foo.com',
            password=self.pwd
        )

    def get_project_serializer_data(self, project):
        serializer = ProjectSerializer(
            project,
            context={'request': self.get_dummy_request()}
        )
        return json.loads(serializer.json_data())

    def test_view_setup(self):
        view = ProjectViewSet()

        self.assertEqual('pk', view.lookup_field)
        self.assertEqual('pk', view.lookup_url_kwarg)
        self.assertEqual(ProjectSerializer, view.serializer_class)
        self.assertEqual(SmallPagination, view.pagination_class)

        qs = Project.objects.all()
        self.assertCountEqual(
            qs, view.queryset
        )
        self.assertEqual(str(qs.query), str(view.queryset.query))

        permission_classes = [ReadPermission, ProjectOwnerPermission]

        self.assertEqual(permission_classes, view.permission_classes)

    def test_inheritance(self):
        classes = (
            APIDefaultsMixin,
            ModelViewSet
        )
        for class_name in classes:
            self.assertTrue(issubclass(ProjectViewSet, class_name))

    def test_view_create(self):
        self.login_test_user(self.user.username)

        project_data = {
            'name': 'another project'
        }
        self.assertFalse(
            Project.objects.filter(
                owner=self.user,
                name=project_data['name']
            ).exists()
        )
        self.client.post(
            reverse(
                'api:project-list'
            ),
            data=project_data
        )
        self.assertTrue(
            Project.objects.filter(
                owner=self.user,
                name=project_data['name']
            ).exists()
        )

    def test_view_detail(self):
        response = self.client.get(
            reverse(
                'api:project-detail',
                kwargs={'pk': self.project.id}
            ),
        )
        data = self.get_project_serializer_data(self.project)

        self.assertEqual(
            data,
            json.loads(response.content)
        )

    def test_view_list(self):
        project_2 = Project.objects.create(
            owner=self.user,
            name='test project 2',
        )
        data_1 = self.get_project_serializer_data(self.project)
        data_2 = self.get_project_serializer_data(project_2)
        expected_results = json.dumps({
            "next": None,
            "previous": None,
            "page_num": 1,
            "count": 2,
            "num_pages": 1,
            "results": [data_1, data_2]
        })
        response = self.client.get(
            reverse('api:project-list')
        )

        self.assertCountEqual(json.loads(expected_results), json.loads(response.content))

    def test_view_update(self):
        self.login_test_user(self.user.username)

        project_data = {'name': 'updated project name'}

        self.assertNotEqual(
            self.project.name,
            project_data['name']
        )

        response = self.client.patch(
            reverse(
                'api:project-detail',
                kwargs={'pk': self.project.id}
            ),
            data=json.dumps(project_data),
            content_type='application/json'
        )
        self.project.refresh_from_db()

        self.assertEqual(response.status_code, drf_status.HTTP_200_OK)
        self.assertEqual(
            self.project.name,
            project_data['name']
        )

    def test_view_delete(self):
        self.login_test_user(self.user.username)

        id = self.project.id

        self.assertTrue(Project.objects.filter(id=id).exists())
        self.client.delete(
            reverse('api:project-detail', kwargs={'pk': self.project.id})
        )
        self.assertFalse(Project.objects.filter(id=id).exists())

    # View permissions
    def test_permissions_create(self):
        project_data = {
            'name': 'test name'
        }

        # Not authenticated
        response = self.client.post(
            reverse(
                'api:project-list'
            ),
            data=project_data
        )

        self.assertEqual(response.status_code, drf_status.HTTP_403_FORBIDDEN)

        # Authenticated
        self.client.logout()
        self.login_test_user(self.user.username)

        response = self.client.post(
            reverse(
                'api:project-list'
            ),
            data=project_data
        )

        self.assertEqual(response.status_code, drf_status.HTTP_201_CREATED)

    def test_permissions_detail(self):
        # Not authenticated
        self.client.logout()

        response = self.client.get(
            reverse(
                'api:project-detail',
                kwargs={'pk': self.project.id}
            ),
        )

        self.assertEqual(response.status_code, drf_status.HTTP_200_OK)

    def test_permissions_list(self):
        # Not authenticated
        self.client.logout()

        response = self.client.get(
            reverse(
                'api:project-list'
            ),
        )

        self.assertEqual(response.status_code, drf_status.HTTP_200_OK)

    def test_permissions_update(self):
        project_data = {'name': 'updated project name'}

        # Not authenticated
        self.client.logout()

        response = self.client.patch(
            reverse(
                'api:project-detail',
                kwargs={'pk': self.project.id}
            ),
            data=json.dumps(project_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, drf_status.HTTP_403_FORBIDDEN)

        # Authenticated not creator
        self.login_test_user(self.user_2.username)

        response = self.client.patch(
            reverse(
                'api:project-detail',
                kwargs={'pk': self.project.id}
            ),
            data=json.dumps(project_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, drf_status.HTTP_403_FORBIDDEN)

        # Creator
        self.client.logout()
        self.login_test_user(self.user.username)

        response = self.client.patch(
            reverse(
                'api:project-detail',
                kwargs={'pk': self.project.id}
            ),
            data=json.dumps(project_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, drf_status.HTTP_200_OK)

        # Superuser not creator
        self.client.logout()
        self.login_test_user(self.superuser.username)

        response = self.client.patch(
            reverse(
                'api:project-detail',
                kwargs={'pk': self.project.id}
            ),
            data=json.dumps(project_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, drf_status.HTTP_200_OK)

    def test_permissions_delete(self):
        # Not authenticated
        self.client.logout()

        response = self.client.delete(
            reverse('api:project-detail', kwargs={'pk': self.project.id})
        )

        self.assertEqual(response.status_code, drf_status.HTTP_403_FORBIDDEN)

        # Authenticated not creator
        self.login_test_user(self.user_2.username)

        response = self.client.delete(
            reverse('api:project-detail', kwargs={'pk': self.project.id})
        )

        self.assertEqual(response.status_code, drf_status.HTTP_403_FORBIDDEN)

        # Creator
        self.client.logout()
        self.login_test_user(self.user.username)

        response = self.client.delete(
            reverse('api:project-detail', kwargs={'pk': self.project.id})
        )

        self.assertEqual(response.status_code, drf_status.HTTP_204_NO_CONTENT)

        # Superuser not creator
        self.project = Project.objects.create(
            owner=self.user,
            name='test project'
        )

        self.client.logout()
        self.login_test_user(self.superuser.username)

        response = self.client.delete(
            reverse('api:project-detail', kwargs={'pk': self.project.id})
        )

        self.assertEqual(response.status_code, drf_status.HTTP_204_NO_CONTENT)


class ProjectImportViewTest(TestCommon):

    def setUp(self):
        super(ProjectImportViewTest, self).setUp()

        project = Project.objects.create(
            owner=self.user,
            name='test project'
        )
        request = self.request_factory.get('/fake-path')
        self.project_data = export_project(project, request)
        project.delete()

    def test_inheritance(self):
        classes = (
            APIDefaultsMixin,
            APIView
        )
        for class_name in classes:
            self.assertTrue(issubclass(ProjectImportView, class_name))

    def test_correct_view_used(self):
        found = resolve(reverse('api:project_import'))
        self.assertEqual(
            found.func.__name__,
            ProjectImportView.as_view().__name__
        )

    def test_view_imports_project_json(self):
        self.login_test_user(self.user.username)
        self.assertFalse(
            Project.objects.filter(
                owner_id=self.user.id,
                name=self.project_data['project']['name'],
            ).exists()
        )
        self.client.post(
            reverse('api:project_import'),
            json.dumps(self.project_data),
            content_type='application/json'
        )
        self.assertTrue(
            Project.objects.filter(
                owner_id=self.user.id,
                name=self.project_data['project']['name'],
            ).exists()
        )
