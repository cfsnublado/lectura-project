import json

from rest_framework import status as drf_status
from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin,
    RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from django.contrib.auth import get_user_model
from django.urls import resolve, reverse

from core.api.views_api import APIDefaultsMixin
from reading.api.pagination import SmallPagination
from reading.api.permissions import (
    ProjectOwnerPermission, ReadingCreatorPermission, ReadPermission
)
from reading.api.views_reading import (
    NestedReadingViewSet, ReadingViewSet, ReadingExportView,
    ReadingImportView
)
from reading.models import Project, Reading
from reading.serializers import ReadingSerializer
from reading.utils import export_reading
from .base_test import TestCommon

User = get_user_model()


class ReadingViewSetTest(TestCommon):

    def setUp(self):
        super(ReadingViewSetTest, self).setUp()

        self.project = Project.objects.create(
            owner=self.user,
            name='test project'
        )
        self.reading = Reading.objects.create(
            creator=self.user,
            project=self.project,
            name='test reading',
            content='test content',
            description='desc',
        )
        self.user_2 = User.objects.create_user(
            username='abc',
            first_name='Christopher',
            last_name='Sanders',
            email='abc@foo.com',
            password=self.pwd
        )

    def get_reading_serializer_data(self, reading):
        serializer = ReadingSerializer(
            reading,
            context={'request': self.get_dummy_request()}
        )
        return json.loads(serializer.json_data())

    def test_view_setup(self):
        view = ReadingViewSet()

        self.assertEqual('pk', view.lookup_field)
        self.assertEqual('pk', view.lookup_url_kwarg)
        self.assertEqual(ReadingSerializer, view.serializer_class)
        self.assertEqual(SmallPagination, view.pagination_class)

        qs = Reading.objects.select_related('project')
        self.assertCountEqual(
            qs, view.queryset
        )
        self.assertEqual(str(qs.query), str(view.queryset.query))

        permission_classes = [ReadPermission, ReadingCreatorPermission]

        self.assertEqual(permission_classes, view.permission_classes)

    def test_inheritance(self):
        classes = (
            APIDefaultsMixin,
            RetrieveModelMixin,
            UpdateModelMixin,
            DestroyModelMixin,
            ListModelMixin,
            GenericViewSet
        )
        for class_name in classes:
            self.assertTrue(issubclass(ReadingViewSet, class_name))

    def test_view_detail(self):
        response = self.client.get(
            reverse(
                'api:reading-detail',
                kwargs={'pk': self.reading.id}
            ),
        )
        data = self.get_reading_serializer_data(self.reading)

        self.assertEqual(
            data,
            json.loads(response.content)
        )

    def test_view_list(self):
        reading_2 = Reading.objects.create(
            creator=self.user,
            project=self.project,
            name='test reading 2',
            content='test content 2'
        )
        data_1 = self.get_reading_serializer_data(self.reading)
        data_2 = self.get_reading_serializer_data(reading_2)
        expected_results = json.dumps({
            "next": None,
            "previous": None,
            "page_num": 1,
            "count": 2,
            "num_pages": 1,
            "results": [data_1, data_2]
        })
        response = self.client.get(
            reverse('api:reading-list')
        )

        self.assertCountEqual(json.loads(expected_results), json.loads(response.content))

    def test_view_update(self):
        self.login_test_user(self.user.username)

        reading_data = {'name': 'updated reading name'}

        self.assertNotEqual(
            self.reading.name,
            reading_data['name']
        )

        response = self.client.patch(
            reverse(
                'api:reading-detail',
                kwargs={'pk': self.reading.id}
            ),
            data=json.dumps(reading_data),
            content_type='application/json'
        )
        self.reading.refresh_from_db()

        self.assertEqual(response.status_code, drf_status.HTTP_200_OK)
        self.assertEqual(
            self.reading.name,
            reading_data['name']
        )

    def test_view_delete(self):
        self.login_test_user(self.user.username)

        id = self.reading.id

        self.assertTrue(Reading.objects.filter(id=id).exists())
        self.client.delete(
            reverse('api:reading-detail', kwargs={'pk': self.reading.id})
        )
        self.assertFalse(Reading.objects.filter(id=id).exists())

    # View permissions
    def test_permissions_detail(self):
        # Not authenticated
        self.client.logout()

        response = self.client.get(
            reverse(
                'api:reading-detail',
                kwargs={'pk': self.reading.id}
            ),
        )

        self.assertEqual(response.status_code, drf_status.HTTP_200_OK)

    def test_permissions_list(self):
        # Not authenticated
        self.client.logout()

        response = self.client.get(
            reverse(
                'api:reading-list'
            ),
        )

        self.assertEqual(response.status_code, drf_status.HTTP_200_OK)

    def test_permissions_update(self):
        reading_data = {'name': 'updated reading name'}

        # Not authenticated
        self.client.logout()

        response = self.client.patch(
            reverse(
                'api:reading-detail',
                kwargs={'pk': self.reading.id}
            ),
            data=json.dumps(reading_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, drf_status.HTTP_403_FORBIDDEN)

        # Authenticated not creator
        self.login_test_user(self.user_2.username)

        response = self.client.patch(
            reverse(
                'api:reading-detail',
                kwargs={'pk': self.reading.id}
            ),
            data=json.dumps(reading_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, drf_status.HTTP_403_FORBIDDEN)

        # Creator
        self.client.logout()
        self.login_test_user(self.user.username)

        response = self.client.patch(
            reverse(
                'api:reading-detail',
                kwargs={'pk': self.reading.id}
            ),
            data=json.dumps(reading_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, drf_status.HTTP_200_OK)

        # Superuser not creator
        self.client.logout()
        self.login_test_user(self.superuser.username)

        response = self.client.patch(
            reverse(
                'api:reading-detail',
                kwargs={'pk': self.reading.id}
            ),
            data=json.dumps(reading_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, drf_status.HTTP_200_OK)

    def test_permissions_delete(self):
        # Not authenticated
        self.client.logout()

        response = self.client.delete(
            reverse('api:reading-detail', kwargs={'pk': self.reading.id})
        )

        self.assertEqual(response.status_code, drf_status.HTTP_403_FORBIDDEN)

        # Authenticated not creator
        self.login_test_user(self.user_2.username)

        response = self.client.delete(
            reverse('api:reading-detail', kwargs={'pk': self.reading.id})
        )

        self.assertEqual(response.status_code, drf_status.HTTP_403_FORBIDDEN)

        # Creator
        self.client.logout()
        self.login_test_user(self.user.username)

        response = self.client.delete(
            reverse('api:reading-detail', kwargs={'pk': self.reading.id})
        )

        self.assertEqual(response.status_code, drf_status.HTTP_204_NO_CONTENT)

        # Superuser not creator
        self.reading = Reading.objects.create(
            creator=self.user,
            project=self.project,
            name='test reading',
            content='hello'
        )

        self.client.logout()
        self.login_test_user(self.superuser.username)

        response = self.client.delete(
            reverse('api:reading-detail', kwargs={'pk': self.reading.id})
        )

        self.assertEqual(response.status_code, drf_status.HTTP_204_NO_CONTENT)


class NestedReadingViewSetTest(TestCommon):

    def setUp(self):
        super(NestedReadingViewSetTest, self).setUp()

        self.project = Project.objects.create(
            owner=self.user,
            name='test project'
        )
        self.project_2 = Project.objects.create(
            owner=self.user,
            name='test project 2'
        )
        self.reading_1 = Reading.objects.create(
            creator=self.user,
            project=self.project,
            name='test reading 1',
            content='test reading 1'
        )
        self.reading_2 = Reading.objects.create(
            creator=self.user,
            project=self.project,
            name='test reading 2',
            content='test reading 2'
        )
        self.reading_3 = Reading.objects.create(
            creator=self.user,
            project=self.project_2,
            name='test reading 3',
            content='test reading 3'
        )
        self.reading_4 = Reading.objects.create(
            creator=self.user,
            project=self.project_2,
            name='test reading 4',
            content='test reading 4'
        )
        self.user_2 = User.objects.create_user(
            username='abc',
            first_name='Christopher',
            last_name='Sanders',
            email='abc@foo.com',
            password=self.pwd
        )

    def get_reading_serializer_data(self, reading):
        serializer = ReadingSerializer(
            reading,
            context={'request': self.get_dummy_request()}
        )
        return json.loads(serializer.json_data())

    def test_view_setup(self):
        view = NestedReadingViewSet()
        self.assertEqual('pk', view.lookup_field)
        self.assertEqual('pk', view.lookup_url_kwarg)
        self.assertEqual(ReadingSerializer, view.serializer_class)
        self.assertEqual(SmallPagination, view.pagination_class)

        qs = Reading.objects.select_related('project')
        self.assertCountEqual(
            qs,
            view.queryset
        )
        self.assertEqual(str(qs.query), str(view.queryset.query))

        permission_classes = [ReadPermission, ProjectOwnerPermission]

        self.assertEqual(permission_classes, view.permission_classes)

    def test_inheritance(self):
        classes = (
            APIDefaultsMixin,
            CreateModelMixin,
            ListModelMixin,
            GenericViewSet
        )
        for class_name in classes:
            self.assertTrue(
                issubclass(NestedReadingViewSet, class_name)
            )

    def test_view_create(self):
        self.login_test_user(self.user.username)

        reading_data = {
            'name': 'test name',
            'content': 'test content'
        }
        self.assertFalse(
            Reading.objects.filter(
                project=self.project,
                name=reading_data['name'],
                content=reading_data['content']
            ).exists()
        )
        self.client.post(
            reverse(
                'api:nested-reading-list',
                kwargs={'project_pk': self.project.id}
            ),
            data=reading_data
        )
        self.assertTrue(
            Reading.objects.filter(
                creator=self.user,
                project=self.project,
                name=reading_data['name'],
                content=reading_data['content']
            ).exists()
        )

    def test_view_list(self):
        self.login_test_user(self.user.username)

        # Source 1
        data_1 = self.get_reading_serializer_data(self.reading_1)
        data_2 = self.get_reading_serializer_data(self.reading_2)
        expected_results = json.dumps({
            "next": None,
            "previous": None,
            "page_num": 1,
            "count": 2,
            "num_pages": 1,
            "results": [data_1, data_2]
        })
        response = self.client.get(
            reverse(
                'api:nested-reading-list',
                kwargs={'project_pk': self.project.id}
            )
        )

        self.assertCountEqual(json.loads(expected_results), json.loads(response.content))

        # Source 2
        data_3 = self.get_reading_serializer_data(self.reading_3)
        data_4 = self.get_reading_serializer_data(self.reading_4)
        expected_results = json.dumps({
            "next": None,
            "previous": None,
            "page_num": 1,
            "count": 2,
            "num_pages": 1,
            "results": [data_3, data_4]
        })
        response = self.client.get(
            reverse(
                'api:nested-reading-list',
                kwargs={'project_pk': self.project_2.id}
            )
        )
        self.assertCountEqual(json.loads(expected_results), json.loads(response.content))

    # Permissions

    def test_permissions_create(self):
        reading_data = {
            'name': 'test name',
            'content': 'test content'
        }

        # Not authenticated
        response = self.client.post(
            reverse(
                'api:nested-reading-list',
                kwargs={'project_pk': self.project.id}
            ),
            data=reading_data
        )

        self.assertEqual(response.status_code, drf_status.HTTP_403_FORBIDDEN)

        # Authenticated not project owner
        self.client.logout()
        self.login_test_user(self.user_2.username)

        response = self.client.post(
            reverse(
                'api:nested-reading-list',
                kwargs={'project_pk': self.project.id}
            ),
            data=reading_data
        )

        self.assertEqual(response.status_code, drf_status.HTTP_403_FORBIDDEN)

        # Source creator
        self.client.logout()
        self.login_test_user(self.user.username)

        response = self.client.post(
            reverse(
                'api:nested-reading-list',
                kwargs={'project_pk': self.project.id}
            ),
            data=reading_data
        )

        self.assertEqual(response.status_code, drf_status.HTTP_201_CREATED)

        # Superuser not project owner
        reading_data = {
            'name': 'another name',
            'content': 'more test content'
        }

        self.client.logout()
        self.login_test_user(self.superuser.username)

        response = self.client.post(
            reverse(
                'api:nested-reading-list',
                kwargs={'project_pk': self.project.id}
            ),
            data=reading_data
        )

        self.assertEqual(response.status_code, drf_status.HTTP_201_CREATED)

    def test_permissions_list(self):
        # Not authenticated
        response = self.client.get(
            reverse(
                'api:nested-reading-list',
                kwargs={'project_pk': self.project.id}
            )
        )

        self.assertEqual(response.status_code, drf_status.HTTP_200_OK)


class ReadingExportViewTest(TestCommon):

    def setUp(self):
        super(ReadingExportViewTest, self).setUp()

        self.project = Project.objects.create(
            owner=self.user,
            name='test project'
        )
        self.reading = Reading.objects.create(
            creator=self.user,
            project=self.project,
            name='test name',
            content='test content'
        )

    def test_inheritance(self):
        classes = (
            APIDefaultsMixin,
            APIView
        )
        for class_name in classes:
            self.assertTrue(issubclass(ReadingExportView, class_name))

    def test_correct_view_used(self):
        found = resolve(
            reverse(
                'api:reading_export',
                kwargs={'reading_pk': self.reading.id}
            )
        )
        self.assertEqual(
            found.func.__name__,
            ReadingExportView.as_view().__name__
        )

    def test_view_setup(self):
        view = ReadingExportView()
        permission_classes = [IsAuthenticated, ReadingCreatorPermission]

        self.assertEqual(permission_classes, view.permission_classes)


class ReadingImportViewTest(TestCommon):

    def setUp(self):
        super(ReadingImportViewTest, self).setUp()

        self.project = Project.objects.create(
            owner=self.user,
            name='test project'
        )
        reading = Reading.objects.create(
            creator=self.user,
            project=self.project,
            name='test name',
            content='test content'
        )
        request = self.request_factory.get('/fake-path')
        self.reading_data = export_reading(reading, request)
        reading.delete()

    def test_inheritance(self):
        classes = (
            APIDefaultsMixin,
            APIView
        )
        for class_name in classes:
            self.assertTrue(issubclass(ReadingExportView, class_name))

    def test_correct_view_used(self):
        found = resolve(reverse('api:reading_import'))
        self.assertEqual(
            found.func.__name__,
            ReadingImportView.as_view().__name__
        )

    def test_view_imports_vocab_source_json(self):
        self.login_test_user(self.user.username)
        self.assertFalse(
            Reading.objects.filter(
                creator_id=self.user.id,
                project__name=self.reading_data['project']['name'],
                name=self.reading_data['reading']['name'],
                content=self.reading_data['reading']['content']
            ).exists()
        )
        self.client.post(
            reverse('api:reading_import'),
            json.dumps(self.reading_data),
            content_type='application/json'
        )
        self.assertTrue(
            Reading.objects.filter(
                creator_id=self.user.id,
                project__name=self.reading_data['project']['name'],
                name=self.reading_data['reading']['name'],
                content=self.reading_data['reading']['content']
            ).exists()
        )
