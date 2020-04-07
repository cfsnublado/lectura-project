from django.contrib.auth import get_user_model
from django.test import TestCase

from core.models import (
    ProjectContentModel, ProjectModel, ProjectPublishMemberModel,
    SerializeModel, SlugifyModel, TimestampModel
)
from ..managers import (
    PostManager, ProjectManager
)
from ..models import (
    Post, PostAudio, Project, ProjectMember
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
            name='Some book',
            description='A good book'
        )


class ProjectTest(TestCommon):

    def setUp(self):
        super(ProjectTest, self).setUp()

    def test_inheritance(self):
        classes = (
            ProjectModel,
        )
        for class_name in classes:
            self.assertTrue(
                issubclass(Project, class_name)
            )

        self.assertIsInstance(Project.objects, ProjectManager)

    def test_string_representation(self):
        self.assertEqual(str(self.project), self.project.name)

    def test_update_slug_on_save(self):
        self.project.name = 'El nombre del viento'
        self.project.full_clean()
        self.project.save()
        self.assertEqual('el-nombre-del-viento', self.project.slug)

    def test_get_serializer(self):
        serializer = self.project.get_serializer()
        self.assertEqual(serializer, ProjectSerializer)

    def test_get_member(self):
        user_2 = User.objects.create_user(
            username='naranjo',
            first_name='Naranjo',
            last_name='Oranges',
            email='naranjo.foo.com',
            password=self.pwd
        )
        user_3 = User.objects.create_user(
            username='manzano',
            first_name='Manzano',
            last_name='Apples',
            email='manzano.foo.com',
            password=self.pwd
        )
        member = ProjectMember.objects.create(
            project=self.project,
            member=user_2
        )

        self.assertEqual(self.project.get_member(user_2), member)
        self.assertIsNone(self.project.get_member(user_3))


class ProjectMemberTest(TestCommon):

    def setUp(self):
        super(ProjectMemberTest, self).setUp()

    def test_inheritance(self):
        classes = (
            ProjectPublishMemberModel,
        )
        for class_name in classes:
            self.assertTrue(
                issubclass(ProjectMember, class_name)
            )

    def test_member_project(self):
        member = ProjectMember.objects.create(
            project=self.project,
            member=self.user
        )
        self.assertTrue(isinstance(member.project, Project))

    def test_get_serializer(self):
        serializer = self.project.get_serializer()
        self.assertEqual(serializer, ProjectSerializer)

    def test_delete_project_member_deletes_posts(self):
        user_2 = User.objects.create_user(
            username='naranjo',
            first_name='Orange',
            last_name='Tree',
            email='naranjo.foo.com',
            password=self.pwd
        )
        member = ProjectMember.objects.create(
            project=self.project,
            member=user_2,
            role=ProjectMember.ROLE_AUTHOR
        )
        post = Post.objects.create(
            creator=user_2,
            project=self.project,
            name='post2',
            content='asdf'
        )
        PostAudio.objects.create(
            creator=user_2,
            post=post,
            name='some audio',
            audio_url='https://foo.com/foo.mp3'
        )
        self.assertTrue(
            Post.objects.filter(
                creator=user_2,
                project=self.project
            ).exists()
        )
        self.assertTrue(
            PostAudio.objects.filter(
                creator=user_2
            ).exists()
        )
        member.delete()
        self.assertFalse(
            Post.objects.filter(
                creator=user_2,
                project=self.project
            ).exists()
        )
        self.assertFalse(
            PostAudio.objects.filter(
                creator=user_2
            ).exists()
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
