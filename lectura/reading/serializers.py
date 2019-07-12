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
    Entry, Project
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


class EntryListSerializer(ListSerializer):
    pass


class EntrySerializer(BaseSerializer, HyperlinkedModelSerializer):
    json_encoder = UUIDEncoder
    minimal_data_fields = [
        'name', 'description', 'date_created'
    ]
    url = HyperlinkedIdentityField(
        view_name='api:entry-detail',
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
        list_serializer = EntryListSerializer
        model = Entry
        fields = (
            'url', 'id', 'project_id', 'project', 'project_slug',
            'project_url', 'creator_id', 'creator_url',
            'name', 'description', 'slug',
            'date_created', 'date_updated'
        )
        read_only_fields = (
            'url', 'id', 'project_id', 'project_slug', 'project_url', 'creator_id', 'creator_url',
            'slug', 'date_created', 'date_updated'
        )

    def create(self, validated_data):
        return Entry.objects.create(**validated_data)


# class VocabEntrySerializer(BaseSerializer, HyperlinkedModelSerializer):
#     json_encoder = UUIDEncoder
#     minimal_data_fields = [
#         'language', 'entry', 'description', 'date_created'
#     ]
#     url = HyperlinkedIdentityField(
#         view_name='api:vocab-entry-detail',
#         lookup_field='pk'
#     )

#     class Meta:
#         list_serializer = ProjectListSerializer
#         model = VocabEntry
#         fields = (
#             'url', 'id', 'language',
#             'entry', 'description',
#             'slug', 'date_created', 'date_updated',
#         )
#         read_only_fields = (
#             'url', 'id', 'slug',
#             'date_created', 'date_updated'
#         )

#     def create(self, validated_data):
#         return VocabEntry.objects.create(**validated_data)


# class VocabContextSerializer(BaseSerializer, HyperlinkedModelSerializer):
#     json_encoder = UUIDEncoder
#     minimal_data_fields = ['content', 'date_created']
#     url = HyperlinkedIdentityField(
#         view_name='api:vocab-context-detail',
#         lookup_field='pk'
#     )
#     vocab_source_url = HyperlinkedRelatedField(
#         many=False,
#         read_only=True,
#         view_name='api:vocab-source-detail',
#         lookup_field='pk',
#         source='vocab_source'
#     )
#     vocab_entries_url = HyperlinkedIdentityField(
#         view_name='api:nested-vocab-context-entry-list',
#         lookup_url_kwarg='vocab_context_pk'
#     )
#     vocab_entry_tags = SerializerMethodField()

#     def get_vocab_entry_tags(self, obj):
#         return obj.get_entries_and_tags()

#     class Meta:
#         model = VocabContext
#         fields = (
#             'url', 'id', 'vocab_source_url',
#             'vocab_source_id', 'content', 'vocab_entries_url',
#             'vocab_entry_tags', 'date_created', 'date_updated',
#         )
#         read_only_fields = (
#             'url', 'id', 'vocab_source_url',
#             'vocab_source_id', 'vocab_entries_url', 'vocab_entry_tags',
#             'date_created', 'date_updated'
#         )

#     def create(self, validated_data):
#         return VocabContext.objects.create(**validated_data)


# class VocabContextEntrySerializer(BaseSerializer, HyperlinkedModelSerializer):
#     minimal_data_fields = [
#         'vocab_entry', 'vocab_context', 'vocab_entry_tags',
#         'date_created'
#     ]
#     url = HyperlinkedIdentityField(
#         view_name='api:vocab-context-entry-detail',
#         lookup_field='pk'
#     )
#     vocab_entry_url = HyperlinkedRelatedField(
#         many=False,
#         read_only=True,
#         view_name='api:vocab-entry-detail',
#         lookup_field='pk',
#         source='vocab_entry'
#     )
#     vocab_entry = StringRelatedField(many=False)
#     vocab_context_url = HyperlinkedRelatedField(
#         many=False,
#         read_only=True,
#         view_name='api:vocab-context-detail',
#         lookup_field='pk',
#         source='vocab_context'
#     )
#     vocab_context = StringRelatedField(many=False)
#     vocab_source_id = ReadOnlyField(source='vocab_context.vocab_source_id')
#     vocab_source_url = HyperlinkedRelatedField(
#         many=False,
#         read_only=True,
#         view_name='api:vocab-source-detail',
#         lookup_field='pk',
#         source='vocab_context.vocab_source'
#     )
#     vocab_source = StringRelatedField(
#         many=False,
#         source='vocab_context.vocab_source'
#     )
#     vocab_source_slug = StringRelatedField(
#         many=False,
#         source='vocab_context.vocab_source.slug'
#     )
#     vocab_entry_tags = StringRelatedField(many=True)

#     class Meta:
#         model = VocabContextEntry
#         fields = (
#             'url', 'id', 'vocab_entry_url', 'vocab_entry_id', 'vocab_entry',
#             'vocab_context_id', 'vocab_context_url',
#             'vocab_context', 'vocab_source_id', 'vocab_source_url', 'vocab_source',
#             'vocab_source_slug', 'date_created',
#             'date_updated', 'vocab_entry_tags'
#         )
#         read_only_fields = (
#             'url', 'id', 'vocab_entry_url', 'vocab_entry_id', 'vocab_context_id',
#             'vocab_context_url', 'vocab_source_id', 'vocab_source_url',
#             'vocab_source', 'vocab_source_slug', 'date_created', 'date_updated'
#         )
