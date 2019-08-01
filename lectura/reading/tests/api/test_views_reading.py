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
    ProjectOwnerPermission, PostCreatorPermission, ReadPermission
)
from reading.api.views_post import (
    NestedPostViewSet, PostViewSet, PostExportView,
    PostImportView
)
from reading.models import Project, Post
from reading.serializers import PostSerializer
from reading.utils import export_post
from .base_test import TestCommon

User = get_user_model()


class PostViewSetTest(TestCommon):

    def setUp(self):
        super(PostViewSetTest, self).setUp()

        self.project = Project.objects.create(
            owner=self.user,
            name='test project'
        )
        self.post = Post.objects.create(
            creator=self.user,
            project=self.project,
            name='test post',
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

    def get_post_serializer_data(self, post):
        serializer = PostSerializer(
            post,
            context={'request': self.get_dummy_request()}
        )
        return json.loads(serializer.json_data())

    def test_view_setup(self):
        view = PostViewSet()

        self.assertEqual('pk', view.lookup_field)
        self.assertEqual('pk', view.lookup_url_kwarg)
        self.assertEqual(PostSerializer, view.serializer_class)
        self.assertEqual(SmallPagination, view.pagination_class)

        qs = Post.objects.select_related('project')
        self.assertCountEqual(
            qs, view.queryset
        )
        self.assertEqual(str(qs.query), str(view.queryset.query))

        permission_classes = [ReadPermission, PostCreatorPermission]

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
            self.assertTrue(issubclass(PostViewSet, class_name))

    def test_view_detail(self):
        response = self.client.get(
            reverse(
                'api:post-detail',
                kwargs={'pk': self.post.id}
            ),
        )
        data = self.get_post_serializer_data(self.post)

        self.assertEqual(
            data,
            json.loads(response.content)
        )

    def test_view_list(self):
        post_2 = Post.objects.create(
            creator=self.user,
            project=self.project,
            name='test post 2',
            content='test content 2'
        )
        data_1 = self.get_post_serializer_data(self.post)
        data_2 = self.get_post_serializer_data(post_2)
        expected_results = json.dumps({
            "next": None,
            "previous": None,
            "page_num": 1,
            "count": 2,
            "num_pages": 1,
            "results": [data_1, data_2]
        })
        response = self.client.get(
            reverse('api:post-list')
        )

        self.assertCountEqual(json.loads(expected_results), json.loads(response.content))

    def test_view_update(self):
        self.login_test_user(self.user.username)

        post_data = {'name': 'updated post name'}

        self.assertNotEqual(
            self.post.name,
            post_data['name']
        )

        response = self.client.patch(
            reverse(
                'api:post-detail',
                kwargs={'pk': self.post.id}
            ),
            data=json.dumps(post_data),
            content_type='application/json'
        )
        self.post.refresh_from_db()

        self.assertEqual(response.status_code, drf_status.HTTP_200_OK)
        self.assertEqual(
            self.post.name,
            post_data['name']
        )

    def test_view_delete(self):
        self.login_test_user(self.user.username)

        id = self.post.id

        self.assertTrue(Post.objects.filter(id=id).exists())
        self.client.delete(
            reverse('api:post-detail', kwargs={'pk': self.post.id})
        )
        self.assertFalse(Post.objects.filter(id=id).exists())

    # View permissions
    def test_permissions_detail(self):
        # Not authenticated
        self.client.logout()

        response = self.client.get(
            reverse(
                'api:post-detail',
                kwargs={'pk': self.post.id}
            ),
        )

        self.assertEqual(response.status_code, drf_status.HTTP_200_OK)

    def test_permissions_list(self):
        # Not authenticated
        self.client.logout()

        response = self.client.get(
            reverse(
                'api:post-list'
            ),
        )

        self.assertEqual(response.status_code, drf_status.HTTP_200_OK)

    def test_permissions_update(self):
        post_data = {'name': 'updated post name'}

        # Not authenticated
        self.client.logout()

        response = self.client.patch(
            reverse(
                'api:post-detail',
                kwargs={'pk': self.post.id}
            ),
            data=json.dumps(post_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, drf_status.HTTP_403_FORBIDDEN)

        # Authenticated not creator
        self.login_test_user(self.user_2.username)

        response = self.client.patch(
            reverse(
                'api:post-detail',
                kwargs={'pk': self.post.id}
            ),
            data=json.dumps(post_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, drf_status.HTTP_403_FORBIDDEN)

        # Creator
        self.client.logout()
        self.login_test_user(self.user.username)

        response = self.client.patch(
            reverse(
                'api:post-detail',
                kwargs={'pk': self.post.id}
            ),
            data=json.dumps(post_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, drf_status.HTTP_200_OK)

        # Superuser not creator
        self.client.logout()
        self.login_test_user(self.superuser.username)

        response = self.client.patch(
            reverse(
                'api:post-detail',
                kwargs={'pk': self.post.id}
            ),
            data=json.dumps(post_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, drf_status.HTTP_200_OK)

    def test_permissions_delete(self):
        # Not authenticated
        self.client.logout()

        response = self.client.delete(
            reverse('api:post-detail', kwargs={'pk': self.post.id})
        )

        self.assertEqual(response.status_code, drf_status.HTTP_403_FORBIDDEN)

        # Authenticated not creator
        self.login_test_user(self.user_2.username)

        response = self.client.delete(
            reverse('api:post-detail', kwargs={'pk': self.post.id})
        )

        self.assertEqual(response.status_code, drf_status.HTTP_403_FORBIDDEN)

        # Creator
        self.client.logout()
        self.login_test_user(self.user.username)

        response = self.client.delete(
            reverse('api:post-detail', kwargs={'pk': self.post.id})
        )

        self.assertEqual(response.status_code, drf_status.HTTP_204_NO_CONTENT)

        # Superuser not creator
        self.post = Post.objects.create(
            creator=self.user,
            project=self.project,
            name='test post',
            content='hello'
        )

        self.client.logout()
        self.login_test_user(self.superuser.username)

        response = self.client.delete(
            reverse('api:post-detail', kwargs={'pk': self.post.id})
        )

        self.assertEqual(response.status_code, drf_status.HTTP_204_NO_CONTENT)


class NestedPostViewSetTest(TestCommon):

    def setUp(self):
        super(NestedPostViewSetTest, self).setUp()

        self.project = Project.objects.create(
            owner=self.user,
            name='test project'
        )
        self.project_2 = Project.objects.create(
            owner=self.user,
            name='test project 2'
        )
        self.post_1 = Post.objects.create(
            creator=self.user,
            project=self.project,
            name='test post 1',
            content='test post 1'
        )
        self.post_2 = Post.objects.create(
            creator=self.user,
            project=self.project,
            name='test post 2',
            content='test post 2'
        )
        self.post_3 = Post.objects.create(
            creator=self.user,
            project=self.project_2,
            name='test post 3',
            content='test post 3'
        )
        self.post_4 = Post.objects.create(
            creator=self.user,
            project=self.project_2,
            name='test post 4',
            content='test post 4'
        )
        self.user_2 = User.objects.create_user(
            username='abc',
            first_name='Christopher',
            last_name='Sanders',
            email='abc@foo.com',
            password=self.pwd
        )

    def get_post_serializer_data(self, post):
        serializer = PostSerializer(
            post,
            context={'request': self.get_dummy_request()}
        )
        return json.loads(serializer.json_data())

    def test_view_setup(self):
        view = NestedPostViewSet()
        self.assertEqual('pk', view.lookup_field)
        self.assertEqual('pk', view.lookup_url_kwarg)
        self.assertEqual(PostSerializer, view.serializer_class)
        self.assertEqual(SmallPagination, view.pagination_class)

        qs = Post.objects.select_related('project')
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
                issubclass(NestedPostViewSet, class_name)
            )

    def test_view_create(self):
        self.login_test_user(self.user.username)

        post_data = {
            'name': 'test name',
            'content': 'test content'
        }
        self.assertFalse(
            Post.objects.filter(
                project=self.project,
                name=post_data['name'],
                content=post_data['content']
            ).exists()
        )
        self.client.post(
            reverse(
                'api:nested-post-list',
                kwargs={'project_pk': self.project.id}
            ),
            data=post_data
        )
        self.assertTrue(
            Post.objects.filter(
                creator=self.user,
                project=self.project,
                name=post_data['name'],
                content=post_data['content']
            ).exists()
        )

    def test_view_list(self):
        self.login_test_user(self.user.username)

        # Post 1
        data_1 = self.get_post_serializer_data(self.post_1)
        data_2 = self.get_post_serializer_data(self.post_2)
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
                'api:nested-post-list',
                kwargs={'project_pk': self.project.id}
            )
        )

        self.assertCountEqual(json.loads(expected_results), json.loads(response.content))

        # Post 2
        data_3 = self.get_post_serializer_data(self.post_3)
        data_4 = self.get_post_serializer_data(self.post_4)
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
                'api:nested-post-list',
                kwargs={'project_pk': self.project_2.id}
            )
        )
        self.assertCountEqual(json.loads(expected_results), json.loads(response.content))

    # Permissions

    def test_permissions_create(self):
        post_data = {
            'name': 'test name',
            'content': 'test content'
        }

        # Not authenticated
        response = self.client.post(
            reverse(
                'api:nested-post-list',
                kwargs={'project_pk': self.project.id}
            ),
            data=post_data
        )

        self.assertEqual(response.status_code, drf_status.HTTP_403_FORBIDDEN)

        # Authenticated not project owner
        self.client.logout()
        self.login_test_user(self.user_2.username)

        response = self.client.post(
            reverse(
                'api:nested-post-list',
                kwargs={'project_pk': self.project.id}
            ),
            data=post_data
        )

        self.assertEqual(response.status_code, drf_status.HTTP_403_FORBIDDEN)

        # Post creator
        self.client.logout()
        self.login_test_user(self.user.username)

        response = self.client.post(
            reverse(
                'api:nested-post-list',
                kwargs={'project_pk': self.project.id}
            ),
            data=post_data
        )

        self.assertEqual(response.status_code, drf_status.HTTP_201_CREATED)

        # Superuser not project owner
        post_data = {
            'name': 'another name',
            'content': 'more test content'
        }

        self.client.logout()
        self.login_test_user(self.superuser.username)

        response = self.client.post(
            reverse(
                'api:nested-post-list',
                kwargs={'project_pk': self.project.id}
            ),
            data=post_data
        )

        self.assertEqual(response.status_code, drf_status.HTTP_201_CREATED)

    def test_permissions_list(self):
        # Not authenticated
        response = self.client.get(
            reverse(
                'api:nested-post-list',
                kwargs={'project_pk': self.project.id}
            )
        )

        self.assertEqual(response.status_code, drf_status.HTTP_200_OK)


class PostExportViewTest(TestCommon):

    def setUp(self):
        super(PostExportViewTest, self).setUp()

        self.project = Project.objects.create(
            owner=self.user,
            name='test project'
        )
        self.post = Post.objects.create(
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
            self.assertTrue(issubclass(PostExportView, class_name))

    def test_correct_view_used(self):
        found = resolve(
            reverse(
                'api:post_export',
                kwargs={'post_pk': self.post.id}
            )
        )
        self.assertEqual(
            found.func.__name__,
            PostExportView.as_view().__name__
        )

    def test_view_setup(self):
        view = PostExportView()
        permission_classes = [IsAuthenticated, PostCreatorPermission]

        self.assertEqual(permission_classes, view.permission_classes)


class PostImportViewTest(TestCommon):

    def setUp(self):
        super(PostImportViewTest, self).setUp()

        self.project = Project.objects.create(
            owner=self.user,
            name='test project'
        )
        post = Post.objects.create(
            creator=self.user,
            project=self.project,
            name='test name',
            content='test content'
        )
        request = self.request_factory.get('/fake-path')
        self.post_data = export_post(post, request)
        post.delete()

    def test_inheritance(self):
        classes = (
            APIDefaultsMixin,
            APIView
        )
        for class_name in classes:
            self.assertTrue(issubclass(PostImportView, class_name))

    def test_correct_view_used(self):
        found = resolve(reverse('api:post_import'))
        self.assertEqual(
            found.func.__name__,
            PostImportView.as_view().__name__
        )

    def test_view_imports_post_json(self):
        self.login_test_user(self.user.username)
        self.assertFalse(
            Post.objects.filter(
                creator_id=self.user.id,
                project__name=self.post_data['project']['name'],
                name=self.post_data['post']['name'],
                content=self.post_data['post']['content']
            ).exists()
        )
        self.client.post(
            reverse('api:post_import'),
            json.dumps(self.post_data),
            content_type='application/json'
        )
        self.assertTrue(
            Post.objects.filter(
                creator_id=self.user.id,
                project__name=self.post_data['project']['name'],
                name=self.post_data['post']['name'],
                content=self.post_data['post']['content']
            ).exists()
        )
