from django.contrib.auth import get_user_model
from django.test import TestCase

from core.models import (
    SerializeModel,
    SlugifyModel, TimestampModel
)
from project.models import Project, ProjectContentModel
from ..managers import (
    PostManager
)
from ..models import (
    Post
)
from ..serializers import (
    PostSerializer
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
            name='Some book',
            description='A good book'
        )


class PostTest(TestCommon):

    def setUp(self):
        super(PostTest, self).setUp()
        self.post = Post.objects.create(
            creator=self.user,
            project=self.project,
            name='Some post',
            content='Hello',
            description='A good post',
        )

    def test_inheritance(self):
        classes = (
            ProjectContentModel, SerializeModel, SlugifyModel,
            TimestampModel
        )
        for class_name in classes:
            self.assertTrue(
                issubclass(Post, class_name)
            )

    def test_manager_type(self):
        self.assertIsInstance(Post.objects, PostManager)

    def test_string_representation(self):
        self.assertEqual(str(self.post), self.post.name)

    def test_update_slug_on_save(self):
        self.post.name = 'El nombre del viento'
        self.post.full_clean()
        self.post.save()
        self.assertEqual('el-nombre-del-viento', self.post.slug)

    def test_get_project(self):
        project = self.post.get_project()
        self.assertEqual(project, self.project)

    def test_get_serializer(self):
        serializer = self.post.get_serializer()
        self.assertEqual(serializer, PostSerializer)
