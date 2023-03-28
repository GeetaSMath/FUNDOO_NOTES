from rest_framework.response import Response
from rest_framework.views import APIView

from .redis_task import RedisNote
from .util import verify_token
from note.models import Note
from note.serializers import NotesSerializer


class NotesAPIView(APIView):
    serializer_class = NotesSerializer

    @verify_token
    def post(self, request):
        try:
            # request.data.update({'user': request.user.id})
            serializer = NotesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # print(request.user.id)
            RedisNote().save(serializer.data)
            return Response(
                {"success": True, "message": "Note Created Successfully", "data": serializer.data, "status": 201},
                status=201)
        except Exception as e:
            return Response({"success": False, "message": e.args[0], "status": 400}, status=400)

    @verify_token
    def get(self, request,note_id : int = None):
        print(note_id)
        try:
            # notes = Note.objects.all()
            # notes = Note.objects.get(id=note_id)
            if note_id is not None:
                redis_note_data = RedisNote().get(note_id,'notes_dict')
            else:
                redis_note_data = RedisNote().get(request.user.id)
            if redis_note_data is not None:
                return Response({'message': "List of Notes", "Data": redis_note_data, "status": 200})
            notes = Note.objects.filter(user=request.user.id)
            serializer = NotesSerializer(notes, many=True)
            return Response(
                {"success": True, "message": "note retrieved Successfully", "data": serializer.data, "status": 200},
                status=200)
        except Exception as e:
            return Response({"success": False, "message": e.args[0], "status": 400}, status=400)

    @verify_token
    def put(self, request):
        try:
            notes = Note.objects.get(id=request.data.get("id"))
            serializer = NotesSerializer(notes, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            RedisNote().save(serializer.data)
            return Response({"success": True, 'message': 'Note updated successfully!', 'Data': serializer.data,
                             "status": 200}, status=200)

        except Exception as e:
            return Response({"success": False, "message": e.args[0], "status": 400}, status=400)

    @verify_token
    def delete(self, request, note_id):
        try:
            notes = Note.objects.get(id=note_id)
            notes.delete()
            RedisNote().delete(note_id)

            return Response({"success": True, "Message": "Note Deleted Successfully", "status": 200}, status=200)
        except Exception as e:
            return Response({"success": False, "message": e.args[0], "status": 400}, status=400)
