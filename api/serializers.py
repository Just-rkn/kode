from rest_framework import serializers
from rest_framework.serializers import ValidationError

from notes.models import Note, NoteAccess, User
from .utils import check_spelling


class NoteSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Note."""

    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def validate_description(self, value):
        errors = check_spelling(value)
        if errors:
            raise ValidationError('В тексте орфографические ошибки.')
        return value

    class Meta:
        model = Note
        fields = ('id', 'title', 'description', 'author')


class NoteAccessSerializer(serializers.ModelSerializer):
    """Сериализатор для модели NoteAccess."""

    class Meta:
        model = NoteAccess
        fields = ('note', 'user', 'access')

    def validate_note(self, note):
        request = self.context['request']
        if not Note.objects.filter(id=note.id).exists():
            raise ValidationError('Заметки не существует.')
        if note.author != request.user:
            raise ValidationError('Только автор может именять доступ.')
        return note

    def validate_user(self, user):
        if not User.objects.filter(id=user.id).exists():
            raise ValidationError('Такого пользователя не существует.')
        return user
