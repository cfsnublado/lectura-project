from .models import Post, Project
from .serializers import (
    PostSerializer, PostAudioSerializer,
    ProjectSerializer
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
        project = Project.objects.get(
            name=project_data['name']
        )
    except Project.DoesNotExist:
        project_serializer = ProjectSerializer(
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
    """
    data: Serialized json data from project backup.
    """
    # validate_project_json_schema(data)

    user_id = user.id
    project_data = data
    post_data = project_data['posts']

    Project.objects.filter(
        owner_id=user_id,
        name=project_data['project_data']['name']
    ).delete()

    project_serializer = ProjectSerializer(
        data=project_data['project_data']
    )
    project_serializer.is_valid(raise_exception=True)
    project = project_serializer.save(
        owner_id=user_id
    )

    for post_dict in post_data:
        post_serializer = PostSerializer(
            data=post_dict['post_data']
        )
        post_serializer.is_valid(raise_exception=True)
        post = post_serializer.save(
            creator_id=user_id,
            project_id=project.id
        )

        for post_audio_dict in post_dict['post_audios']:
            post_audio_serializer = PostAudioSerializer(
                data=post_audio_dict['post_audio_data']
            )
            post_audio_serializer.is_valid(raise_exception=True)
            post_audio_serializer.save(
                creator_id=user.id,
                post_id=post.id
            )


def export_post(post, request=None):
    '''
    Generates a serialized backup of a post.
    '''
    project_serializer = ProjectSerializer(
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
    project_serializer = ProjectSerializer(
        project,
        context={'request': request}
    )
    project_dict = {
        'project_data': project_serializer.get_minimal_data()
    }
    project_dict['posts'] = []

    for post in project.posts.all():
        post_serializer = PostSerializer(
            post,
            context={'request': request}
        )
        post_dict = {
            'post_data': post_serializer.get_minimal_data()
        }
        post_dict['post_audios'] = []

        for post_audio in post.post_audios.all():
            post_audio_serializer = PostAudioSerializer(
                post_audio,
                context={'request': request}
            )
            post_dict['post_audios'].append(
                {
                    'post_audio_data': post_audio_serializer.get_minimal_data()
                }
            )

        project_dict['posts'].append(post_dict)

    return project_dict
