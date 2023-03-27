from rest_framework import serializers

from note.models import Note


class NotesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = ['id', 'user', 'title', 'description', 'isArchive', 'isTrash', 'color', 'image', 'label',
                  'collaborator', 'reminder']
        read_only_fields = ['label', 'collaborator']
