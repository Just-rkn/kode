from rest_framework import permissions

from notes.models import NoteAccess


class IsAuthorOrHasNoteAccess(permissions.BasePermission):
    """
    Проверяет, является ли пользователь автором заметки или имеет к ней доступ.
    """

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True

        try:
            note_access = obj.accessible_users.get(user=request.user)
            if request.method in permissions.SAFE_METHODS:
                return note_access.access in ('read', 'update')
            if request.method.lower() in ('put', 'patch'):
                return note_access.access == 'update'
            return False
        except NoteAccess.DoesNotExist:
            return False
