from rest_framework import serializers
from rest_framework import serializers

from note.models import Labels, Note

from note.models import Note
from drf_yasg import openapi
from rest_framework import serializers


class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'user', 'title', 'description', 'isArchive', 'isTrash', 'color', 'image', 'label',
                  'collaborator', 'reminder']
        read_only_fields = ['label', 'collaborator']
        swagger_schema_fields = {
            "required": ['title', 'description', 'isArchive', 'isTrash', 'color', 'label',
                         'collaborator'], "type": openapi.TYPE_OBJECT,
            "properties": {
                # "user": openapi.Schema(
                #     title="user",
                #     type=openapi.TYPE_STRING,
                # ),
                "title": openapi.Schema(
                    title="title",
                    type=openapi.TYPE_STRING,
                ),
                "description": openapi.Schema(
                    title="description",
                    type=openapi.TYPE_STRING,
                ),
                "isArchive": openapi.Schema(
                    title="isArchive",
                    type=openapi.TYPE_STRING,
                ),
                "isTrash": openapi.Schema(
                    title="isTrash",
                    type=openapi.TYPE_STRING,
                ),
                "color": openapi.Schema(
                    title="color",
                    type=openapi.TYPE_STRING,
                ),
                "label": openapi.Schema(
                    title="label",
                    type=openapi.TYPE_STRING,
                ),
                "collaborator": openapi.Schema(
                    title="collaborator",
                    type=openapi.TYPE_STRING,
                ),

            }}


class LabelSerializer(serializers.ModelSerializer):
    """
     Class for label serializer
    """

    class Meta:
        model = Labels
        fields = ['id', 'user', 'name']
        swagger_schema_fields = {
            "required": ['user', 'name'], "type": openapi.TYPE_OBJECT,
            "properties": {
                # "user": openapi.Schema(
                #     title="user",
                #     type=openapi.TYPE_STRING,
                # ),
                "user": openapi.Schema(
                    user="user",
                    type=openapi.TYPE_STRING,
                ),
                "name": openapi.Schema(
                    title="name",
                    type=openapi.TYPE_STRING,
                ),

            }}


#
# class NoteSerializer(serializers.ModelSerializer):
#     labels = serializers.StringRelatedField(many=True)
#
#     # label = LabelsSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Note
#         fields = ('id', 'title', 'content', 'labels')


class LabelViewSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'label', 'user')
    #
    # def create(self, validated_data):
    #     note_id = self.initial_data.get('id')
    #     note = Note.objects.get(id=note_id, user=validated_data['user'])
    #     [note.label.add(i.id) for i in validated_data['label']]
    #     return note
