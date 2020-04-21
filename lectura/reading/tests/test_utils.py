import json

from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase

from ..models import (
    Post, PostAudio, Project
)
from ..serializers import (
    PostSerializer, PostAudioSerializer,
    ProjectSerializer
)
from ..utils import (
    export_post, export_project,
    import_post, import_project,
    validate_project_json_schema
)

User = get_user_model()


class TestCommon(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.pwd = 'Pizza?69p'
        self.user = User.objects.create_superuser(
            username='cfs',
            first_name='Christopher',
            last_name='Sanders',
            email='cfs7@foo.com',
            password=self.pwd
        )


class ExportProjectTest(TestCommon):

    def setUp(self):
        super(ExportProjectTest, self).setUp()
        self.request = self.request_factory.get('/fake-path')
        self.request.user = self.user

    def test_export_project_data(self):
        project = Project.objects.create(
            owner=self.user,
            name='Test project',
        )
        post = Post.objects.create(
            creator=self.user,
            project=project,
            name='Test post',
            content='This is a test post.'
        )
        post_audio = PostAudio.objects.create(
            creator=self.user,
            post=post,
            name='test-audio',
            audio_url='https://foo.foo/test-audio.mp3'
        )
        project_serializer = ProjectSerializer(
            project,
            context={'request': self.request}
        )
        post_serializer = PostSerializer(
            post,
            context={'request': self.request}
        )
        post_audio_serializer = PostAudioSerializer(
            post_audio,
            context={'request': self.request}
        )
        expected_data = json.loads(json.dumps({
            'project_data': project_serializer.get_minimal_data(),
            'posts': [
                {
                    'post_data': post_serializer.get_minimal_data(),
                    'post_audios': [
                        {
                            'post_audio_data': post_audio_serializer.get_minimal_data(),
                        }
                    ]
                }
            ]
        }))
        data = export_project(project, request=self.request)
        self.assertEqual(expected_data, data)


class ImportProjectTest(TestCommon):

    def setUp(self):
        super(ImportProjectTest, self).setUp()
        self.request = self.request_factory.get('/fake-path')
        self.request.user = self.user

    def test_import_project_data(self):
        project = Project.objects.create(
            owner=self.user,
            name='Test project',
        )
        post = Post.objects.create(
            creator=self.user,
            project=project,
            name='Test post',
            content='This is a test post.'
        )
        post_audio = PostAudio.objects.create(
            creator=self.user,
            post=post,
            name='test-audio',
            audio_url='https://foo.foo/test-audio.mp3'
        )

        data = export_project(project, request=self.request)
        Project.objects.all().delete()
        self.assertEqual(len(Project.objects.all()), 0)
        self.assertEqual(len(Post.objects.all()), 0)
        self.assertEqual(len(PostAudio.objects.all()), 0)
        import_project(data, self.user)
        self.assertEqual(len(Project.objects.all()), 1)
        project = Project.objects.get(
            owner=self.user,
            name='Test project',
        )
        post = Post.objects.get(
            creator=self.user,
            project=project,
            name='Test post',
            content='This is a test post.'
        )
        post_audio = PostAudio.objects.get(
            creator=self.user,
            post=post,
            name='test-audio',
            audio_url='https://foo.foo/test-audio.mp3'
        )


class ExportPostTest(TestCommon):

    def setUp(self):
        super(ExportPostTest, self).setUp()
        self.request = self.request_factory.get('/fake-path')
        self.request.user = self.user

    def test_export_post_data(self):
        project = Project.objects.create(
            owner=self.user,
            name='Test project',
        )
        post = Post.objects.create(
            creator=self.user,
            project=project,
            name='Test post',
            content='This is a test post.'
        )
        post_audio = PostAudio.objects.create(
            creator=self.user,
            post=post,
            name='test-audio',
            audio_url='https://foo.foo/test-audio.mp3'
        )
        project_serializer = ProjectSerializer(
            project,
            context={'request': self.request}
        )
        post_serializer = PostSerializer(
            post,
            context={'request': self.request}
        )
        post_audio_serializer = PostAudioSerializer(
            post_audio,
            context={'request': self.request}
        )
        expected_data = json.loads(json.dumps({
            'project_data': project_serializer.get_minimal_data(),
            'post_data': post_serializer.get_minimal_data(),
            'post_audios': [
                {
                    'post_audio_data': post_audio_serializer.get_minimal_data(),
                }
            ]
        }))
        data = export_post(post, request=self.request)
        self.assertEqual(expected_data, data)


class ImportPostTest(TestCommon):

    def setUp(self):
        super(ImportPostTest, self).setUp()
        self.request = self.request_factory.get('/fake-path')
        self.request.user = self.user

    def test_import_post_data(self):
        project = Project.objects.create(
            owner=self.user,
            name='Test project',
        )
        post = Post.objects.create(
            creator=self.user,
            project=project,
            name='Test post',
            content='This is a test post.'
        )
        post_audio = PostAudio.objects.create(
            creator=self.user,
            post=post,
            name='test-audio',
            audio_url='https://foo.foo/test-audio.mp3'
        )

        data = export_post(post, request=self.request)
        Project.objects.all().delete()
        self.assertEqual(len(Project.objects.all()), 0)
        self.assertEqual(len(Post.objects.all()), 0)
        self.assertEqual(len(PostAudio.objects.all()), 0)

        import_post(data, self.user)
        self.assertEqual(len(Project.objects.all()), 1)

        project = Project.objects.get(
            owner=self.user,
            name='Test project',
        )
        post = Post.objects.get(
            creator=self.user,
            project=project,
            name='Test post',
            content='This is a test post.'
        )
        post_audio = PostAudio.objects.get(
            creator=self.user,
            post=post,
            name='test-audio',
            audio_url='https://foo.foo/test-audio.mp3'
        )


class ValidateProjectJSONTest(TestCommon):

    def setUp(self):
        super(ValidateProjectJSONTest, self).setUp()
        self.request = self.request_factory.get('/fake-path')
        self.request.user = self.user

    def test_validate_vocab_source_data(self):
        # Note: Test further for exceptions.

        project = Project.objects.create(
            owner=self.user,
            name='Test project',
        )
        post = Post.objects.create(
            creator=self.user,
            project=project,
            name='Test post',
            content='This is a test post.'
        )
        post_audio = PostAudio.objects.create(
            creator=self.user,
            post=post,
            name='test-audio',
            audio_url='https://foo.foo/test-audio.mp3'
        )
        project_serializer = ProjectSerializer(
            project,
            context={'request': self.request}
        )
        post_serializer = PostSerializer(
            post,
            context={'request': self.request}
        )
        post_audio_serializer = PostAudioSerializer(
            post_audio,
            context={'request': self.request}
        )
        data = {
            'project_data': project_serializer.get_minimal_data(),
            'posts': [
                {
                    'post_data': post_serializer.get_minimal_data(),
                    'post_audios': [
                        {
                            'post_audio_data': post_audio_serializer.get_minimal_data(),
                        }
                    ]
                }
            ]
        }
        validate_project_json_schema(json.loads(json.dumps(data)))

        data = {
            'project_data': project_serializer.get_minimal_data(),
            'posts': [
                {
                    'post_data': post_serializer.get_minimal_data(),
                    'post_audios': []
                }
            ]
        }
        validate_project_json_schema(json.loads(json.dumps(data)))
