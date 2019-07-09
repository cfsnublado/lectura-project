import uuid

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from coretest.models import (
    TestTimestampModel, TestUUIDModel
)

User = get_user_model()

# Testing abstract classes in core using test models from coretest.


class UUIDModelTest(TestCase):
    def setUp(self):
        self.test_model = TestUUIDModel.objects.create(name='hello')

    def test_id_is_uuid(self):
        self.assertIsInstance(self.test_model.id, uuid.UUID)

    def test_pk_is_uuid(self):
        self.assertIsInstance(self.test_model.pk, uuid.UUID)
        self.assertEqual(self.test_model.pk, self.test_model.id)

    def test_set_uuid_on_create(self):
        test_id = uuid.uuid4()
        test_model = TestUUIDModel.objects.create(id=test_id, name='hello')
        self.assertEqual(test_model.id, test_id)


class TimestampModelTest(TestCase):

    def test_datetime_on_create_and_update(self):
        test_model = TestTimestampModel.objects.create(name='hello')
        created = test_model.date_created
        updated = test_model.date_updated
        self.assertEqual(
            (created.year, created.month, created.day, created.hour, created.minute),
            (updated.year, updated.month, updated.day, updated.hour, updated.minute)
        )
        test_model.name = 'good bye'
        test_model.save()
        self.assertGreater(test_model.date_updated, updated)

    def test_date_created_provided_on_create(self):
        date_created = timezone.now() + timezone.timedelta(hours=-48, minutes=-1, seconds=-1)
        test_model = TestTimestampModel.objects.create(
            name='hello',
            date_created=date_created
        )
        self.assertEqual(test_model.date_created, date_created)
        self.assertGreater(test_model.date_updated, test_model.date_created)
