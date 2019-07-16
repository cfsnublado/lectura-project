from rest_framework.serializers import (
    HyperlinkedIdentityField, HyperlinkedRelatedField,
    HyperlinkedModelSerializer,
    ListSerializer, ReadOnlyField, StringRelatedField
)

from django.contrib.auth import get_user_model

from core.serializers import (
    BaseSerializer, UUIDEncoder
)
from .models import (
    Reading, Project
)

User = get_user_model()


class ProjectListSerializer(ListSerializer):
    pass


class ProjectSerializer(BaseSerializer, HyperlinkedModelSerializer):
    json_encoder = UUIDEncoder
    minimal_data_fields = [
        'name', 'description', 'date_created'
    ]
    url = HyperlinkedIdentityField(
        view_name='api:project-detail',
        lookup_field='pk'
    )
    owner_id = ReadOnlyField(source='owner.id')
    owner_url = HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='api:user-detail',
        lookup_field='username',
        source='owner'
    )

    class Meta:
        list_serializer = ProjectListSerializer
        model = Project
        fields = (
            'url', 'id', 'owner_id', 'owner_url',
            'name', 'description', 'slug', 'date_created', 'date_updated',
        )
        read_only_fields = (
            'url', 'id', 'owner_id', 'owner_url',
            'slug', 'date_created', 'date_updated'
        )

    def create(self, validated_data):
        return Project.objects.create(**validated_data)


class ReadingListSerializer(ListSerializer):
    pass


class ReadingSerializer(BaseSerializer, HyperlinkedModelSerializer):
    json_encoder = UUIDEncoder
    minimal_data_fields = [
        'name', 'description', 'date_created'
    ]
    url = HyperlinkedIdentityField(
        view_name='api:reading-detail',
        lookup_field='pk'
    )
    project_id = ReadOnlyField(source='project_id')
    project_url = HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='api:project-detail',
        lookup_field='pk',
        source='project'
    )
    project = StringRelatedField(
        many=False,
        source='project.name'
    )
    project_slug = StringRelatedField(
        many=False,
        source='project.slug'
    )
    creator_id = ReadOnlyField(source='creator.id')
    creator_url = HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='api:user-detail',
        lookup_field='username',
        source='creator'
    )

    class Meta:
        list_serializer = ReadingListSerializer
        model = Reading
        fields = (
            'url', 'id', 'project_id', 'project', 'project_slug',
            'project_url', 'creator_id', 'creator_url',
            'name', 'description', 'content', 'slug',
            'date_created', 'date_updated'
        )
        read_only_fields = (
            'url', 'id', 'project_id', 'project_slug', 'project_url', 'creator_id', 'creator_url',
            'slug', 'date_created', 'date_updated'
        )

    def create(self, validated_data):
        return Reading.objects.create(**validated_data)
