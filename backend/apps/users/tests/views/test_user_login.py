import pytest

from rest_framework import status
from rest_framework.authtoken.models import Token

from apps.users.models import User


@pytest.mark.django_db
@pytest.mark.parametrize(
    'email_or_username', [
        ('email'),
        ('username'),
    ]
)
def test_user_login_success(client, api_auth_endpoints, generate_user_data, email_or_username):
    user_data = generate_user_data()

    response = client.post(
        api_auth_endpoints['register'],
        user_data,
    )
    assert response.status_code == status.HTTP_201_CREATED
    user = response.json().get('user')
    old_token = response.json().get('token')
    assert old_token

    response = client.post(
        api_auth_endpoints['login'],
        {
            'email_or_username': user[email_or_username],
            'password': user_data['password'],
        },
    )
    assert response.status_code == status.HTTP_200_OK

    user = response.json().get('user')
    assert user.get('email') == user_data.get('email')
    assert user.get('username')
    assert 'password' not in user
    assert 'id' in user

    user_obj = User.objects.get(id=user.get('id'))
    assert user_obj.email == user.get('email')
    assert user_obj.username == user.get('username')

    token = response.json().get('token')
    assert old_token != token
    assert not Token.objects.filter(key=old_token).exists()

    token_obj = Token.objects.get(key=token)
    assert token_obj.user == user_obj


@pytest.mark.django_db
@pytest.mark.parametrize(
    'email_or_username, password', [
        ('', 'Password123'),      # missing email
        ('user@test.com', ''),    # missing password
    ]
)
def test_user_login_failure_missing_fields(client, api_auth_endpoints, email_or_username, password):
    response = client.post(api_auth_endpoints['login'], {
        'email_or_username': email_or_username,
        'password': password,
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    data = response.json()
    if email_or_username == '':
        assert 'This field may not be blank.' in data.get('email_or_username')
    if password == '':
        assert 'This field may not be blank.' in data.get('password')


@pytest.mark.django_db
@pytest.mark.parametrize(
    'email_or_username, password', [
        ('nonexistent_email@test.com', 'Password123'),  # invalid email
        ('nonexistent_user', 'Password123'),            # invalid username
    ]
)
def test_user_login_failure_invalid_inputs(client, api_auth_endpoints, email_or_username, password):
    response = client.post(api_auth_endpoints['login'], {
        'email_or_username': email_or_username,
        'password': password,
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'non_field_errors' in response.json()
    assert 'Unable to log in with provided credentials.' in response.json()['non_field_errors']
