from .models import Post, ReadingProject
from .serializers import (
    PostSerializer, ReadingProjectSerializer
)


def import_post(data, user):
    '''
    data: Serialized json data from post backup.
    '''
    # validate_post_json_schema(data)

    user_id = user.id
    project_data = data['project']
    post_data = data['post']

    Post.objects.filter(
        creator_id=user_id,
        name=post_data['name']
    ).delete()

    post_serializer = PostSerializer(
        data=post_data
    )
    post_serializer.is_valid(raise_exception=True)

    try:
        project = ReadingProject.objects.get(
            name=project_data['name']
        )
    except ReadingProject.DoesNotExist:
        project_serializer = ReadingProjectSerializer(
            data=project_data
        )
        project_serializer.is_valid(raise_exception=True)
        project = project_serializer.save(
            owner_id=user_id
        )

    post_serializer.save(
        creator_id=user_id,
        project_id=project.id
    )


def import_project(data, user):
    '''
    data: Serialized json data from project backup.
    '''
    # validate_project_json_schema(data)

    user_id = user.id
    project_data = data['project']
    post_data = data['posts']

    ReadingProject.objects.filter(
        owner_id=user_id,
        name=project_data['name']
    ).delete()

    project_serializer = ReadingProjectSerializer(
        data=project_data
    )
    project_serializer.is_valid(raise_exception=True)
    project = project_serializer.save(
        owner_id=user_id
    )

    for post in post_data:
        post_serializer = PostSerializer(
            data=post
        )
        post_serializer.is_valid(raise_exception=True)
        post_serializer.save(
            creator_id=user_id,
            project_id=project.id
        )


def export_post(post, request=None):
    '''
    Generates a serialized backup of a post.
    '''
    project_serializer = ReadingProjectSerializer(
        post.project,
        context={'request': request}
    )
    post_serializer = PostSerializer(
        post,
        context={'request': request}
    )
    post_dict = {
        'project': project_serializer.get_minimal_data(),
        'post': post_serializer.get_minimal_data()
    }

    return post_dict


def export_project(project, request=None):
    project_serializer = ReadingProjectSerializer(
        project,
        context={'request': request}
    )
    project_dict = {
        'project': project_serializer.get_minimal_data(),
        'posts': []
    }

    for post in project.posts.all():
        post_serializer = PostSerializer(
            post,
            context={'request': request}
        )
        project_dict['posts'].append(post_serializer.get_minimal_data())

    return project_dict
