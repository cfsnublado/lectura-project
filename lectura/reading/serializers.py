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
    Post, PostAudio, ReadingProject
)

User = get_user_model()


class ReadingProjectListSerializer(ListSerializer):
    pass


class ReadingProjectSerializer(BaseSerializer, HyperlinkedModelSerializer):
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
    posts_url = HyperlinkedIdentityField(
        view_name="api:nested-post-list",
        lookup_url_kwarg="project_pk",
        lookup_field="pk"
    )

    class Meta:
        list_serializer = ReadingProjectListSerializer
        model = ReadingProject
        fields = (
            'url', 'id', 'owner_id', 'owner_url',
            'name', 'description', 'slug', 'posts_url',
            'date_created', 'date_updated',
        )
        read_only_fields = (
            'url', 'id', 'owner_id', 'owner_url',
            'slug', 'posts_url',
            'date_created', 'date_updated'
        )

    def create(self, validated_data):
        return ReadingProject.objects.create(**validated_data)


class PostListSerializer(ListSerializer):
    pass


class PostSerializer(BaseSerializer, HyperlinkedModelSerializer):
    json_encoder = UUIDEncoder
    minimal_data_fields = [
        'name', 'description', 'content',
        'date_created'
    ]
    url = HyperlinkedIdentityField(
        view_name='api:post-detail',
        lookup_field='pk'
    )
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
    post_audios_url = HyperlinkedIdentityField(
        view_name="api:nested-post-audio-list",
        lookup_url_kwarg="post_pk",
        lookup_field="pk"
    )

    class Meta:
        list_serializer = PostListSerializer
        model = Post
        fields = (
            'url', 'id', 'project_id', 'project', 'project_slug',
            'project_url', 'creator_id', 'creator_url',
            'name', 'description', 'content', 'slug', 'post_audios_url',
            'date_created', 'date_updated'
        )
        read_only_fields = (
            'url', 'id', 'project_id', 'project_slug', 'project_url',
            'creator_id', 'creator_url', 'slug', 'post_audios_url',
            'date_created', 'date_updated'
        )

    def create(self, validated_data):
        return Post.objects.create(**validated_data)


class PostAudioListSerializer(ListSerializer):
    pass


class PostAudioSerializer(BaseSerializer, HyperlinkedModelSerializer):
    json_encoder = UUIDEncoder
    minimal_data_fields = [
        'name', 'url', 'date_created'
    ]
    url = HyperlinkedIdentityField(
        view_name='api:post-audio-detail',
        lookup_field='pk'
    )
    post_url = HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='api:post-detail',
        lookup_field='pk',
        source='post'
    )
    post = StringRelatedField(
        many=False,
        source='post.name'
    )
    post_slug = StringRelatedField(
        many=False,
        source='post.slug'
    )
    creator_id = ReadOnlyField(source='creator.id')
    creator_username = ReadOnlyField(source='creator.username')
    creator_url = HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='api:user-detail',
        lookup_field='username',
        source='creator'
    )

    class Meta:
        list_serializer = PostAudioListSerializer
        model = PostAudio
        fields = (
            'url', 'id', 'post_id', 'post', 'post_slug',
            'post_url', 'creator_id', 'creator_username',
            'creator_url', 'name', 'audio_url', 'slug',
            'date_created', 'date_updated'
        )
        read_only_fields = (
            'url', 'id', 'post_id', 'post_slug', 'post_url',
            'creator_id', 'creator_url', 'slug',
            'date_created', 'date_updated'
        )
