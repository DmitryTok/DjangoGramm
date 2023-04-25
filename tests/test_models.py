import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from djangogramm_app.models import Pictures


@pytest.fixture
def user_data():
    # Define test user data
    return {
        'email': 'test@example.com',
        'username': 'testuser',
        'full_name': 'Test User',
        'bio': 'Test user bio',
        'avatar': Pictures.objects.create(picture='test_image.jpg'),
        'is_email_verify': True,
    }


@pytest.fixture
def user(user_data):
    # Create a new user and return it
    user = get_user_model().objects.create_user(**user_data)
    return user


def test_user_model(user_data, user, db, clear_db):
    assert user.email == user_data['email']
    assert user.username == user_data['username']
    assert user.full_name == user_data['full_name']
    assert user.bio == user_data['bio']
    assert user.avatar == user_data['avatar']
    assert user.is_email_verify == user_data['is_email_verify']

    # Test __str__ method
    assert str(user) == user_data['email']

    # Test constraints
    with pytest.raises(ValidationError):
        get_user_model().objects.create_user(
            email='test@example.com',
            username='testuser2',
            full_name='Test User 2',
            bio='Test user bio 2',
            avatar=user_data['avatar'],
            is_email_verify=True,
        )
