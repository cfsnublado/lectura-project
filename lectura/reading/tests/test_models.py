from django.contrib.auth import get_user_model
from django.test import TestCase

from core.models import (
    SerializeModel,
    SlugifyModel, TimestampModel
)
from ..managers import (
    ReadingManager
)
from ..models import (
    CreatorModel, Project, ProjectContentModel, Reading
)
from ..serializers import (
    ReadingSerializer
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


class ReadingTest(TestCommon):

    def setUp(self):
        super(ReadingTest, self).setUp()
        self.project = Project.objects.create(
            owner=self.user,
            name='Some book',
            description='A good book'
        )
        self.reading = Reading.objects.create(
            creator=self.user,
            project=self.project,
            name='Some reading',
            content='Hello',
            description='A good reading',
        )

    def test_inheritance(self):
        classes = (
            ProjectContentModel, SerializeModel, SlugifyModel,
            TimestampModel, CreatorModel
        )
        for class_name in classes:
            self.assertTrue(
                issubclass(Reading, class_name)
            )

    def test_manager_type(self):
        self.assertIsInstance(Reading.objects, ReadingManager)

    def test_string_representation(self):
        self.assertEqual(str(self.reading), self.reading.name)

    def test_update_slug_on_save(self):
        self.reading.name = 'El nombre del viento'
        self.reading.full_clean()
        self.reading.save()
        self.assertEqual('el-nombre-del-viento', self.reading.slug)

    def test_get_project(self):
        project = self.reading.get_project()
        self.assertEqual(project, self.project)

    def test_get_serializer(self):
        serializer = self.reading.get_serializer()
        self.assertEqual(serializer, ReadingSerializer)
