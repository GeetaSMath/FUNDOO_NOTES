import json
from django.db.models import Q
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from .redis_task import RedisNote
from .util import verify_token
from note.models import Note, Labels
from user_fundoo.models import User
from note.serializers import NotesSerializer, LabelSerializer, LabelViewSetSerializer
from rest_framework import viewsets
from rest_framework import status



class NotesAPIView(APIView):
    serializer_class = NotesSerializer

    @swagger_auto_schema(request_body=NotesSerializer, operation_summary='POST Notes')
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

    @swagger_auto_schema(operation_summary='Get Notes', responses={200: 'OK', 400: 'BAD REQUEST'})
    @verify_token
    def get(self, request):
        try:
            notes = Note.objects.filter(
                Q(user=request.user.id) | Q(collaborator__id=request.user.id) | Q(label__id=request.user.id),
                isTrash=False, isArchive=False).distinct()
            serializer = NotesSerializer(notes, many=True)
            return Response(
                {"success": True, "message": "note retrieved Successfully", "data": serializer.data, "status": 200},
                status=200)

        except Exception as e:
            return Response({"success": False, "message": e.args[0], "status": 400}, status=400)

    @swagger_auto_schema(request_body=NotesSerializer, responses={201: 'Created', 400: 'BAD REQUEST'})
    @verify_token
    def put(self, request):
        try:
            notes = Note.objects.get(id=request.data.get("note_id"))
            serializer = NotesSerializer(notes, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            RedisNote().save(serializer.data)
            return Response({"success": True, 'message': 'Note updated successfully!', 'Data': serializer.data,
                             "status": 200}, status=200)

        except Exception as e:
            return Response({"success": False, "message": e.args[0], "status": 400}, status=400)

    @swagger_auto_schema(operation_summary="delete note")
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
    @swagger_auto_schema(request_body=NotesSerializer, responses={201: 'Created', 400: 'BAD REQUEST'})
    def post(self, request, *args, **kwargs):
        try:
            response = self.create(request, *args, **kwargs)
            return Response({"message": "Label Created Successfully", "data": response.data, "status": 201})
        except Exception as e:
            return Response({"message": str(e)}, status=400)

    @verify_token
    @swagger_auto_schema(operation_summary='Get Notes', responses={200: 'OK', 400: 'BAD REQUEST'})
    def get(self, request, *args, **kwargs):
        try:
            response = self.list(request, *args, **kwargs)
            return Response({"Message": "List of Labels", "data": response.data, "status": 200})
        except Exception as e:
            return Response({"Message": str(e)}, status=400)

    @verify_token
    @swagger_auto_schema(request_body=NotesSerializer, responses={201: 'Created', 400: 'BAD REQUEST'})
    def put(self, request, *args, **kwargs):
        try:
            response = self.update(request, *args, **kwargs)
            return Response({"Message": "Label Updated Successfully", "data": response.data, "status": 200})
        except Exception as e:
            return Response({"Message": str(e)}, status=400)

    @verify_token
    @swagger_auto_schema(operation_summary="delete note")
    def delete(self, request, *args, **kwargs):
        try:
            response = self.destroy(request, *args, **kwargs)
            return Response({"message": "Label Deleted Successfully", "data": response.data, "status": 200})
        except Exception as e:
            return Response({"message": str(e)}, status=400)


# collaborator add and delete operation
class Collaborator(APIView):
    @verify_token
    @swagger_auto_schema(request_body=NotesSerializer, operation_summary='POST Notes')
    def post(self, request, id):
        try:
            note = Note.objects.get(id=id, user=request.user.id)
            user_id = request.data.get('collaborator')
            c_user = User.objects.get(id=user_id)
            if request.user.email != c_user.email:
                note.collaborator.add(c_user)
            return Response({"message": "Collaborator Added Successfully", 'status': 201})
        except Exception as e:
            return Response({"message": str(e)}, status=400)

    @verify_token
    @swagger_auto_schema(operation_summary="delete note")
    def delete(self, request, id):
        try:
            note = Note.objects.get(id=id, user=request.user.id)
            user_id = request.data.get('collaborator')
            c_user = User.objects.get(id=user_id)
            if note.collaborator.filter(id=c_user.id).exists():
                note.collaborator.remove(c_user)
                return Response({"message": "Collaborator Deleted Successfully", 'status': 200})
            else:
                return Response({"message": "Collaborator not found", 'status': 404})
        except Exception as e:
            return Response({"message": str(e)}, status=400)


class LabelNote(viewsets.ModelViewSet):
    serializer_class = LabelViewSetSerializer

    @verify_token
    def create(self, request):
        try:
            serializer = LabelViewSetSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"success": True, "message": "Note label Created Successfully", "data": serializer.data, "status": 201},
                status=201)
        except Exception as e:
            return Response({"success": False, "message": e.args[0], "status": 400}, status=400)

    @verify_token
    def destroy(self, request, pk):
        try:
            label_rm = Note.objects.get(id=pk)
            label_rm.delete()
            return Response({"message": "label note Deleted Successfully", 'status': 200})
        except Exception as e:
            return Response({"message": str(e)}, status=400)
