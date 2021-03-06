import json

from rest_framework.reverse import reverse as drf_reverse

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from project.models import Project
from ..models import (
    Post
)
from ..serializers import (
    PostSerializer, ProjectSerializer
)

User = get_user_model()


class TestCommon(TestCase):

    def setUp(self):
        self.pwd = 'Pizza?69p'
        self.user = User.objects.create_user(
            username='cfs',
            first_name='Christopher',
            last_name='Sanders',
            email='cfs7@cfs.com',
            password=self.pwd
        )
        self.project = Project.objects.create(
            owner=self.user,
            name='Test Project',
            description='A test project'
        )


class ProjectSerializerTest(TestCommon):

    def setUp(self):
        super(ProjectSerializerTest, self).setUp()
        self.request = self.client.get(reverse('api:project-list')).wsgi_request
        self.serializer = ProjectSerializer(
            self.project,
            context={'request': self.request}
        )

    def test_minimal_data_fields(self):
        expected_minimal_data = [
            'name', 'description', 'date_created'
        ]
        self.assertCountEqual(expected_minimal_data, self.serializer.minimal_data_fields)

    def test_get_minimal_data(self):
        expected_data = {
            'name': self.project.name,
            'description': self.project.description,
            'date_created': self.project.date_created.isoformat()
        }
        self.assertEqual(expected_data, self.serializer.get_minimal_data())

    def test_serialized_data(self):
        expected_data = {
            'url': drf_reverse(
                'api:project-detail',
                kwargs={'pk': self.project.id},
                request=self.request
            ),
            'id': self.project.id,
            'owner_id': self.user.id,
            'owner_url': drf_reverse(
                'api:user-detail',
                kwargs={'username': self.user.username},
                request=self.request
            ),
            'name': self.project.name,
            'description': self.project.description,
            'slug': self.project.slug,
            'date_created': self.project.date_created.isoformat(),
            'date_updated': self.project.date_updated.isoformat(),
        }
        data = self.serializer.data
        self.assertEqual(expected_data, data)

    def test_json_data(self):
        expected_json_data = json.dumps({
            'url': drf_reverse(
                'api:project-detail',
                kwargs={'pk': self.project.pk},
                request=self.request
            ),
            'id': self.project.id,
            'owner_id': str(self.user.id),
            'owner_url': drf_reverse(
                'api:user-detail',
                kwargs={'username': self.user.username},
                request=self.request
            ),
            'name': self.project.name,
            'description': self.project.description,
            'slug': self.project.slug,
            'date_created': self.project.date_created.isoformat(),
            'date_updated': self.project.date_updated.isoformat(),
        })
        json_data = self.serializer.json_data()
        self.assertEqual(json.loads(expected_json_data), json.loads(json_data))

    def test_validation_no_name(self):
        data = {'name': ''}
        self.serializer = ProjectSerializer(self.project, data=data, partial=True)
        self.assertFalse(self.serializer.is_valid())
        self.assertEqual(len(self.serializer.errors), 1)
        self.assertTrue(self.serializer.errors['name'])


class PostSerializerTest(TestCommon):

    def setUp(self):
        super(PostSerializerTest, self).setUp()
        self.post = Post.objects.create(
            creator=self.user,
            project=self.project,
            name='Test Post',
            content='Hello',
            description='A test post'
        )
        self.request = self.client.get(reverse('api:post-list')).wsgi_request
        self.serializer = PostSerializer(
            self.post,
            context={'request': self.request}
        )

    def test_minimal_data_fields(self):
        expected_minimal_data = [
            'name', 'description', 'content',
            'date_created'
        ]
        self.assertCountEqual(expected_minimal_data, self.serializer.minimal_data_fields)

    def test_get_minimal_data(self):
        expected_data = {
            'name': self.post.name,
            'description': self.post.description,
            'content': self.post.content,
            'date_created': self.post.date_created.isoformat()
        }
        self.assertEqual(expected_data, self.serializer.get_minimal_data())

    def test_serialized_data(self):
        expected_data = {
            'url': drf_reverse(
                'api:post-detail',
                kwargs={'pk': self.post.id},
                request=self.request
            ),
            'id': self.post.id,
            'project_id': self.project.id,
            'project_url': drf_reverse(
                'api:project-detail',
                kwargs={'pk': self.project.id},
                request=self.request
            ),
            'project': self.project.name,
            'project_slug': self.project.slug,
            'creator_id': self.user.id,
            'creator_url': drf_reverse(
                'api:user-detail',
                kwargs={'username': self.user.username},
                request=self.request
            ),
            'name': self.post.name,
            'description': self.post.description,
            'slug': self.post.slug,
            'content': self.post.content,
            'date_created': self.post.date_created.isoformat(),
            'date_updated': self.post.date_updated.isoformat(),
        }
        data = self.serializer.data
        self.assertEqual(expected_data, data)

    def test_json_data(self):
        expected_json_data = json.dumps({
            'url': drf_reverse(
                'api:post-detail',
                kwargs={'pk': self.post.pk},
                request=self.request
            ),
            'id': self.post.id,
            'project_id': self.project.id,
            'project_url': drf_reverse(
                'api:project-detail',
                kwargs={'pk': self.project.pk},
                request=self.request
            ),
            'project': self.project.name,
            'project_slug': self.project.slug,
            'creator_id': str(self.user.id),
            'creator_url': drf_reverse(
                'api:user-detail',
                kwargs={'username': self.user.username},
                request=self.request
            ),
            'name': self.post.name,
            'description': self.post.description,
            'slug': self.post.slug,
            'content': self.post.content,
            'date_created': self.post.date_created.isoformat(),
            'date_updated': self.post.date_updated.isoformat(),
        })
        json_data = self.serializer.json_data()
        self.assertEqual(json.loads(expected_json_data), json.loads(json_data))

    def test_validation_no_name(self):
        data = {'name': ''}
        self.serializer = PostSerializer(self.post, data=data, partial=True)
        self.assertFalse(self.serializer.is_valid())
        self.assertEqual(len(self.serializer.errors), 1)
        self.assertTrue(self.serializer.errors['name'])
