from .models import Project, Reading
from .serializers import (
    ProjectSerializer, ReadingSerializer
)


def import_reading(data, user):
    '''
    data: Serialized json data from reading backup.
    '''
    # validate_reading_json_schema(data)

    user_id = user.id
    project_data = data['project']
    reading_data = data['reading']

    Reading.objects.filter(
        creator_id=user_id,
        name=reading_data['name']
    ).delete()

    reading_serializer = ReadingSerializer(
        data=reading_data
    )
    reading_serializer.is_valid(raise_exception=True)

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

    reading_serializer.save(
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
    reading_data = data['readings']

    Project.objects.filter(
        owner_id=user_id,
        name=project_data['name']
    ).delete()

    project_serializer = ProjectSerializer(
        data=project_data
    )
    project_serializer.is_valid(raise_exception=True)
    project = project_serializer.save(
        owner_id=user_id
    )

    for reading in reading_data:
        reading_serializer = ReadingSerializer(
            data=reading
        )
        reading_serializer.is_valid(raise_exception=True)
        reading_serializer.save(
            creator_id=user_id,
            project_id=project.id
        )


def export_reading(reading, request=None):
    '''
    Generates a serialized backup of a reading.
    '''
    project_serializer = ProjectSerializer(
        reading.project,
        context={'request': request}
    )
    reading_serializer = ReadingSerializer(
        reading,
        context={'request': request}
    )
    reading_dict = {
        'project': project_serializer.get_minimal_data(),
        'reading': reading_serializer.get_minimal_data()
    }

    return reading_dict


def export_project(project, request=None):
    project_serializer = ProjectSerializer(
        project,
        context={'request': request}
    )
    project_dict = {
        'project': project_serializer.get_minimal_data(),
        'readings': []
    }

    for reading in project.readings.all():
        reading_serializer = ReadingSerializer(
            reading,
            context={'request': request}
        )
        project_dict['readings'].append(reading_serializer.get_minimal_data())

    return project_dict
