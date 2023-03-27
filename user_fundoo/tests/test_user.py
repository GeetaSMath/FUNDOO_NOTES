import pytest
from django.urls import reverse

REGISTER_URL = reverse('register')
LOGIN_URL = reverse('login')

@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(first_name="geeta",
                                                 email='g@gmail.com', password='123@geeta',
                                                 mobile_number=2972630725)


@pytest.fixture
def user_data():
    return {
        'first_name': 'geeta',
        'email': 'g@gmail.com',
        'password': '123@geeta',
        'mobile_number': 2972630725}


@pytest.fixture
def user_data_error():
    return {
        'first_name1': 'geeta',
        'email': 'c@gmail.com',
        'password': 'c',
        'mobile_number': 2972630725}


@pytest.fixture
def user_login_data():
    return {'email':'g@gmail.com' , 'password': '123@geeta'}


@pytest.fixture
def user_login_data_error():
    return {'username': 'geeta', 'password': '123'}


class TestUserLoginAndRegister:
    def test_user_registration_successfully(self, db, client, django_user_model, user_data):
        response = client.post(REGISTER_URL, user_data, content_type="application/json")
        assert response.status_code == 201

    #@pytest.mark.xyz
    @pytest.mark.django_db
    def test_user_registration_unsuccessfully(self, client, django_user_model, user_data_error):
        response = client.post(REGISTER_URL, user_data_error, content_type="application/json")
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_user_login_successfully(self,django_user_model, client, user_login_data, user):
        response = client.post(LOGIN_URL, user_login_data, content_type="application/json")
        print(django_user_model.objects.all())
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_user_login_unsuccessfully(self, client, user, user_login_data_error):
        response = client.post(LOGIN_URL, user_login_data_error, content_type="application/json")
        assert response.status_code == 400
