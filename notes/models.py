from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Note(models.Model):
    """Модель заметки."""

    title = models.CharField('Название', max_length=255)
    description = models.TextField('Текст')
    author = models.ForeignKey(
        User,
        related_name='notes',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    access_users = models.ManyToManyField(
        User, related_name='accessible_notes', through='NoteAccess'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'


class NoteAccess(models.Model):
    """Модель прав доступа к заметке."""

    class AccessType(models.TextChoices):
        """Типы доступа к заметкам."""

        READ = 'read'
        UPDATE = 'update'

    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        related_name='accessible_users',
        verbose_name='Заметка'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователь'
    )
    access = models.CharField(
        max_length=30, choices=AccessType.choices, verbose_name='Доступ'
    )

    def __str__(self):
        return f'Доступ {self.access} у {self.user} к {self.note}'

    class Meta:
        verbose_name = 'Доступ к заметке'
        verbose_name_plural = 'Доступ к заметкам'
