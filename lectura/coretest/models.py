from django.db import models

from core.models import (
    TimestampModel, UserstampModel, UUIDModel
)

# These models are only used for testing purposes. They are to be migrated only into the test db.


class BaseTestModel(models.Model):
    name = models.CharField(
        max_length=100,
        default="hello",
    )

    class Meta:
        abstract = True


class TestModel(BaseTestModel):
    pass


class TestColorModel(BaseTestModel):
    RED = 1
    BLUE = 2
    GREEN = 3

    COLOR_CHOICES = (
        (RED, "Red"),
        (BLUE, "Blue"),
        (GREEN, "Green")
    )

    color = models.IntegerField(
        choices=COLOR_CHOICES,
        default=GREEN
    )


class TestUserstampModel(BaseTestModel, UserstampModel):

    def get_absolute_url(self):
        return "/"


class TestTimestampModel(BaseTestModel, TimestampModel):
    pass


class TestUUIDModel(BaseTestModel, UUIDModel):
    pass
