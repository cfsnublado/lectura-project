from .serializers import (
    ProjectSerializer, ReadingSerializer
)


def export_reading(request=None, reading=None):
    '''
    Generates a serialized backup of a reading.
    '''
    if reading:
        project_serializer = ProjectSerializer(
            reading.project,
            context={'request': request}
        )
        reading_serializer = ReadingSerializer(
            reading,
            context={'request': request}
        )
        reading_dict = {
            'project_data': project_serializer.get_minimal_data(),
            'reading_data': reading_serializer.get_minimal_data()
        }

        return reading_dict
