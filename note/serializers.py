from rest_framework import serializers
from rest_framework import serializers

from note.models import Labels, Note

from note.models import Note


class NotesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = ['id', 'user', 'title', 'description', 'isArchive', 'isTrash', 'color', 'image', 'label',
                  'collaborator', 'reminder']
        read_only_fields = ['label', 'collaborator']

class LabelSerializer(serializers.ModelSerializer):
    """
     Class for label serializer
    """

    class Meta:
        model = Labels
        fields = ['id', 'user', 'name']


