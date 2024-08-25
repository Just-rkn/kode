from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsAuthorOrHasNoteAccess
from api.serializers import NoteAccessSerializer, NoteSerializer
from notes.models import Note, NoteAccess


class NoteViewsSet(viewsets.ModelViewSet):
    """ViewSet для управления заметками."""

    serializer_class = NoteSerializer

    def get_permissions(self):
        if self.action == 'list':
            return (IsAuthenticated(),)
        return (IsAuthenticated(), IsAuthorOrHasNoteAccess())

    def get_queryset(self):
        if self.action == 'list':
            user = self.request.user
            return Note.objects.filter(
                Q(author=user) |
                Q(
                    accessible_users__user=user,
                    accessible_users__access__in=('read', 'update')
                )
            ).distinct()
        return Note.objects.all()


class NoteAccessView(APIView):
    """APIView для управления доступом к заметками."""

    def post(self, request, *args, **kwargs):
        serializer = NoteAccessSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        note_id = request.data.get('note')
        user_id = request.data.get('user')

        if not note_id or not user_id:
            return Response(
                {'detail': 'Поля note и user необходимо заполнить.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        note_access = get_object_or_404(NoteAccess, note=note_id, user=user_id)
        if note_access.task.author != request.user:
            return Response(
                {'detail': 'Только автор может изменять доступ.'},
                status=status.HTTP_403_FORBIDDEN
            )
        note_access.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
