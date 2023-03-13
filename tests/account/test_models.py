from django.conf import settings


class TestUser:
    def test_settings(self):
        assert "apps.accounts" in settings.INSTALLED_APPS
        assert "accounts.User" == settings.AUTH_USER_MODEL
