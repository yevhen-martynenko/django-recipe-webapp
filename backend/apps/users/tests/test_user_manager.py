import pytest
from apps.users.models import User


@pytest.mark.django_db
def test_create_user_success(generate_user_data):
    user_data = generate_user_data()

    user = User.objects.create_user(
        email=user_data['email'],
        username='',
        description='Test description',
        password=user_data['password'],
    )
    assert user.email == user_data['email']
    assert user.username == user_data['email'].split('@')[0]
    assert user.description == 'Test description'
    assert user.check_password(user_data['password'])
    assert user.is_active is True


@pytest.mark.django_db
def test_create_user_without_email(generate_user_data):
    user_data = generate_user_data()

    with pytest.raises(ValueError, match='Users must have an email address'):
        User.objects.create_user(
            email='',
            username='',
            description='Test description',
            password=user_data['password'],
        )


@pytest.mark.django_db
def test_create_superuser_success(generate_user_data):
    user_data = generate_user_data()
    
    user = User.objects.create_superuser(
        email=user_data['email'],
        password=user_data['password'],
    )
    assert user.email == user_data['email']
    assert user.username == user_data['email'].split('@')[0]
    assert user.check_password(user_data['password'])
    assert user.is_active is True
    assert user.is_superuser is True
    assert user.is_staff is True
    assert user.is_admin is True


@pytest.mark.django_db
@pytest.mark.parametrize(
    'email, password, expected_error',
    [
        ('', '1', 'Superusers must have an email address'),
        ('admin@test.com', None, 'Superusers must have a password.'),
    ]
)
def test_create_superuser_missing_fields(email, password, expected_error):
    with pytest.raises(ValueError, match=expected_error):
        User.objects.create_superuser(email=email, password=password)
