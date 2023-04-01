from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

from .redis_task import RedisNote
from .util import verify_token
from note.models import Note, Labels
from note.serializers import NotesSerializer, LabelSerializer


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
    def get(self, request, note_id: int = None):
        print(note_id)
        try:
            # notes = Note.objects.all()
            # notes = Note.objects.get(id=note_id)
            if note_id is not None:
                redis_note_data = RedisNote().get(note_id, 'notes_dict')
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


class LabelCreate(GenericAPIView, CreateModelMixin, DestroyModelMixin, ListModelMixin, UpdateModelMixin):
    """
    Class for create and retrieve label using mixins
    """
    queryset = Labels.objects.all()
    serializer_class = LabelSerializer

    @verify_token
    def post(self, request, *args, **kwargs):
        try:
            response = self.create(request, *args, **kwargs)
            return Response({"message": "Label Created Successfully", "data": response.data, "status": 201})
        except Exception as e:
            return Response({"message": str(e)}, status=400)

    @verify_token
    def get(self, request, *args, **kwargs):
        try:
            response = self.list(request, *args, **kwargs)
            return Response({"Message": "List of Labels", "data": response.data, "status": 200})
        except Exception as e:
            return Response({"Message": str(e)}, status=400)

    @verify_token
    def put(self, request, *args, **kwargs):
        try:
            response = self.update(request, *args, **kwargs)
            return Response({"Message": "Label Updated Successfully", "data": response.data, "status": 200})
        except Exception as e:
            return Response({"Message": str(e)}, status=400)

    @verify_token
    def delete(self, request, *args, **kwargs):
        try:
            response = self.destroy(request, *args, **kwargs)
            return Response({"message": "Label Deleted Successfully", "data": response.data, "status": 200})
        except Exception as e:
            return Response({"message": str(e)}, status=400)


# collaborator add and delete operation
class Collaborator(APIView):
    @verify_token
    def post(self, request, id):
        try:
            User = get_user_model()
            print(request.user.id, 1213334)
            print(id)
            note = Note.objects.get(id=id, user=request.user.id)
            user_id = request.data.get('collaborator')
            user_name = request.user.email
            print(user_name)
            print(note)
            print(user_id)
            c_user = User.objects.get(id=user_id)
            # c_user = User.objects.get(email=user_name)
            print(c_user)
            if request.user.email != c_user:
                note.collaborator.add(c_user)
            return Response({"message": "Collaborator Added Successfully", 'status': 201})
        except Exception as e:
            return Response({"message": str(e)}, status=400)




    @verify_token
    def delete(self, request, id):
        try:
            note = Note.objects.get(id=id, user=request.user.id)
            user_name = request.data.get('collaborator')
            user = User.objects.get(username=user_name)
            if request.user.id != user:
                note.collaborator.remove(user)
            return Response({"message": "Collaborator Deleted Successfully", 'status': 200})
        except Exception as e:
            return Response({"message": str(e)}, status=400)


