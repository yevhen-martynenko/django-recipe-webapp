import pytest

from apps.users.serializers import UserRegisterSerializer


@pytest.mark.django_db
def test_serializer_valid_data():
    valid_data = {
        'email': 'test@test.com',
        'username': '',
        'password': 'Password019283',
    }

    serializer = UserRegisterSerializer(data=valid_data)
    assert serializer.is_valid()
    assert serializer.validated_data['email'] == 'test@test.com'


@pytest.mark.django_db
def test_serializer_valid_data_with_username():
    valid_data = {
        'email': 'test@test.com',
        'username': 'test',
        'password': 'Password019283',
    }

    serializer = UserRegisterSerializer(data=valid_data)
    assert serializer.is_valid()
    assert serializer.validated_data['email'] == 'test@test.com'
    assert serializer.validated_data['username'] == 'test'


@pytest.mark.django_db
def test_serializer_invalid_email():
    invalid_data = {
        'email': 'invalid_email',
        'username': 'test',
        'password': 'Password019283',
    }

    serializer = UserRegisterSerializer(data=invalid_data)
    assert not serializer.is_valid()
    assert 'email' in serializer.errors
    assert 'Enter a valid email address' in serializer.errors['email'][0]


@pytest.mark.django_db
def test_serializer_empty_password():
    invalid_data = {
        'email': 'test@test.com',
        'username': 'test',
        'password': '',
    }

    serializer = UserRegisterSerializer(data=invalid_data)
    assert not serializer.is_valid()
    assert 'password' in serializer.errors
    assert 'This field may not be blank.' in serializer.errors['password'][0]
