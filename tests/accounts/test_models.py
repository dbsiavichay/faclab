import pytest
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class TestUser:
    def test_settings(self):
        assert "apps.accounts" in settings.INSTALLED_APPS
        assert "accounts.User" == settings.AUTH_USER_MODEL

    @pytest.mark.django_db
    def test_create_user(self):
        user = User.objects.create(
            username="test",
            email="test@test.com",
            first_name="Test",
            last_name="User",
            password="test",
        )

        assert isinstance(user, User)
        assert user.is_active
        assert not user.is_staff
        assert not user.is_superuser
        assert "Test User" == user.get_full_name()
        assert "Test" == user.get_short_name()
        assert user.username == str(user)
