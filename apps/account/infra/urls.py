from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import path

urlpatterns = (
    path(
        route="login/",
        view=LoginView.as_view(
            template_name="account/login.html", redirect_authenticated_user=True
        ),
        name="login",
    ),
    path(route="logout/", view=LogoutView.as_view(), name="logout"),
    path(
        route="user/password/reset/",
        view=PasswordResetView.as_view(template_name="account/reset.html"),
        name="password_reset",
    ),
    path(
        route="user/password/reset/done/",
        view=PasswordResetDoneView.as_view(
            template_name="account/reset_password_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        route="reset/<uidb64>/<token>/",
        view=PasswordResetConfirmView.as_view(
            success_url="/user/reset/done/",
            template_name="account/reset_password_complete.html",
        ),
        name="password_reset_confirm",
    ),
    path(
        route="user/reset/done/",
        view=PasswordResetCompleteView.as_view(
            template_name="account/reset_password_done_complete.html"
        ),
        name="password_reset_complete",
    ),
)
