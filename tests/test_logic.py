import pytest
from http import HTTPStatus

from .api_endpoints import GET_NOTES_URL, SET_ACCESS_URL


@pytest.mark.django_db
def test_note_access_creation(
    authenticated_user_client, authenticated_author_client,
    note, access_data
):
    response = authenticated_user_client.get(f'{GET_NOTES_URL}{note.id}/')
    assert response.status_code == HTTPStatus.FORBIDDEN
    response = authenticated_author_client.post(
        SET_ACCESS_URL, data=access_data
    )
    assert response.status_code == HTTPStatus.CREATED
    response = authenticated_user_client.get(f'{GET_NOTES_URL}{note.id}/')
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_note_visibility(
    authenticated_author_client, authenticated_user_client,
    author, note
):
    # Получаем начальное количество заметок у пользователя и автора
    response = authenticated_user_client.get(GET_NOTES_URL)
    user_notes_before = len(response.json())
    response = authenticated_author_client.get(GET_NOTES_URL)
    author_notes_before = len(response.json())

    new_note_data = {
        'title': 'test title',
        'description': 'test description'
    }
    response = authenticated_author_client.post(
        GET_NOTES_URL, data=new_note_data
    )
    assert response.status_code == HTTPStatus.CREATED

    response = authenticated_user_client.get(GET_NOTES_URL)
    assert len(response.json()) == user_notes_before

    response = authenticated_author_client.get(GET_NOTES_URL)
    assert len(response.json()) == author_notes_before + 1


@pytest.mark.django_db
def test_note_speller(authenticated_author_client):
    note_data_with_text_error = {
        'title': 'test title',
        'description': 'Тут есть ашибка.'
    }
    new_note_data = {
        'title': 'test title',
        'description': 'Тут нет ошибок.'
    }
    response = authenticated_author_client.post(
        GET_NOTES_URL, data=new_note_data
    )
    assert response.status_code == HTTPStatus.CREATED

    response = authenticated_author_client.post(
        GET_NOTES_URL, data=note_data_with_text_error
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
