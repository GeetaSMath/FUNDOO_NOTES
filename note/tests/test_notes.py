import pytest
from django.urls import reverse
from note.models import Note

credential = {"email": 'geeta@gmail.com', "password": 'geeta@123'}
login_url = reverse('login')
note_body = lambda user_id: {'title': 'Python programming',
                             'description': 'Python is the most popular language now days.', 'user_id': user_id}
empty_note_body = lambda user_id: {}
invalid_note_body = lambda user_id: {'title123': 'Python programming',
                                     'description2': 'Python is the most popular language now days.',
                                     'user_id': user_id}

NOTE_URL = reverse('notes')


@pytest.fixture
def headers(client, db, django_user_model):
    user = django_user_model.objects.create_user(**credential)
    login_response = client.post(login_url, credential, content_type="application/json")
    return {'HTTP_TOKEN': login_response.json()['token'], "content_type": "application/json", 'user': user}


@pytest.fixture
def note_obj(client, db, headers):
    user = headers.pop('user')
    payload: dict = note_body(user.id)
    invalid_data_payload: dict = invalid_note_body(user.id)
    return Note.objects.create(**payload)


"""

{'success': True, 'message': 'Note Created Successfully',
        'data': {'id': 1, 'user': 1, 'title': 'Python programming',
                 'description': 'Python is the most popular language now days.', 'isArchive': False, 'isTrash': False,
                 'color': None, 'image': None, 'label': [], 'collaborator': [], 'reminder': None}, 
        'status': 200}

"""


class TestNotesAPI:
    """
        Test Notes API
    """

    # @pytest.mark.xyz
    @pytest.mark.django_db
    def test_response_as_create_notes_successfully(self, headers, db, client, django_user_model):
        user = headers.pop('user')
        payload: dict = note_body(user.id)
        response = client.post(NOTE_URL, payload, **headers)
        data = response.json()
        assert isinstance(data['data'], dict)
        assert response.status_code == 201
        assert data['data']['title'] == payload['title']

    # @pytest.mark.xyz
    @pytest.mark.django_db
    def test_response_as_create_notes_unsuccessfully(self, headers, db, client, django_user_model):
        response = client.post(NOTE_URL, empty_note_body, **headers)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_response_as_create_invalid_notes_unsuccessfully(self, headers, db, client, django_user_model):
        user = headers.pop('user')
        invalid_data_payload: dict = invalid_note_body(user.id)
        response = client.post(NOTE_URL, invalid_data_payload, **headers)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_response_as_retriv_note_successfully(self, headers, db, client, django_user_model):
        response = client.get(NOTE_URL, **headers)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_update_note_successfully(self, headers, db, client, django_user_model):
        user = headers.pop('user')
        payload: dict = note_body(user.id)
        response = client.post(NOTE_URL, payload, **headers)
        data = response.json()
        notes_id = data.get('data').get('id')
        updated_note_data = {
            'title': 'Updated Note',
            'description': 'This is an updated note'
        }
        update_url = reverse('note_id', args=[notes_id])
        response = client.put(update_url, data=updated_note_data, **headers, format='json')
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_update_note_with_invalid_data_unsuccessfully(self, headers, db, client, django_user_model):
        user = headers.pop('user')
        payload: dict = note_body(user.id)
        response = client.post(NOTE_URL, payload, **headers)
        data = response.json()
        notes_id = data.get('data').get('id')
        updated_note_data = {
            'title123': 'Updated Note',
            'description23': 'This is an updated note'
        }
        update_url = reverse('note_id', args=[notes_id])
        response = client.put(update_url, data=updated_note_data, **headers, format='json')
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_update_note_without_note_unsuccessfully(self, headers, db, client, django_user_model):
        response = client.post(NOTE_URL, empty_note_body, **headers)
        data = response.json()
        notes_id = data.get('data')
        updated_note_data = {
            'title': 'Updated Note',
            'description': 'This is an updated note'
        }
        update_url = reverse('note_id', args=[15])
        response = client.put(update_url, data=updated_note_data, **headers, format='json')
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_delete_note_success(self, headers, db, client, django_user_model):
        user = headers.pop('user')
        payload: dict = note_body(user.id)
        response = client.post(NOTE_URL, payload, **headers)
        data = response.json()
        notes_id = data.get('data').get('id')
        delete_url = reverse('note_id', args=[notes_id])
        res = client.delete(delete_url, **headers)
        assert res.status_code == 200
        assert Note.objects.count() == 0

    @pytest.mark.django_db
    def test_delete_note_unsuccessfully(self, headers, db, client, django_user_model):
        user = headers.pop('user')
        payload: dict = note_body(user.id)
        response = client.post(NOTE_URL, payload, **headers)
        data = response.json()
        notes_id = data.get('data').get('id')
        delete_url = reverse('note_id', args=[13])
        res = client.delete(delete_url, **headers)
        assert res.status_code == 400
        # assert Note.objects.count() == 0
